#!/usr/bin/env python
"""Script to handle migration issues and apply new migrations."""

import os
import sys
import django
from django.conf import settings

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zolits_backend.settings')
django.setup()

from django.core.management import call_command
from django.db import connection, models
from django.apps import apps

print("=" * 60)
print("Migration Helper Script")
print("=" * 60)

# Check if the phone_number column exists in userprofile
print("\nChecking database state...")
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT column_name FROM information_schema.columns 
        WHERE table_name = 'core_userprofile' AND column_name = 'phone_number'
    """)
    phone_number_exists = cursor.fetchone() is not None
    print(f"  phone_number column exists: {phone_number_exists}")
    
    cursor.execute("""
        SELECT column_name FROM information_schema.columns 
        WHERE table_name = 'core_issue' AND column_name = 'resolved_by_id'
    """)
    resolved_by_exists = cursor.fetchone() is not None
    print(f"  resolved_by column exists: {resolved_by_exists}")

# Check migration table
print("\nChecking applied migrations...")
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT app, name FROM django_migrations 
        WHERE app = 'core' ORDER BY applied
    """)
    migrations = cursor.fetchall()
    for app, name in migrations:
        print(f"  - {name}")

# Mark 0003 as applied if it's not already
print("\nApplying pending migrations...")
if phone_number_exists:
    print("  Marking 0003_userprofile_phone_number as applied (table already exists)...")
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO django_migrations (app, name, applied)
            VALUES ('core', '0003_userprofile_phone_number', NOW())
            ON CONFLICT DO NOTHING
        """)
        connection.commit()

# Apply the new 0004 migration
if not resolved_by_exists:
    print("  Applying 0004_issue_resolved_by migration...")
    try:
        call_command('migrate', 'core', '0004_issue_resolved_by', verbosity=2)
        print("  Migration applied successfully!")
    except Exception as e:
        print(f"  Error applying migration: {e}")
else:
    print("  resolved_by column already exists, skipping migration.")

print("\n" + "=" * 60)
print("Migration check complete!")
print("=" * 60)
