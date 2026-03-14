import os
import sys
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zolits_backend.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.db import connection
from django.db.migrations.recorder import MigrationRecorder

print("Recording 0003 migration as applied...")
recorder = MigrationRecorder(connection)
try:
    recorder.record_applied('core', '0003_userprofile_phone_number')
    print("✓ 0003_userprofile_phone_number marked as applied")
except Exception as e:
    print(f"Note: {e}")

print("\nApplying remaining migrations...")
from django.core.management import call_command
try:
    result = call_command('migrate', 'core')
    print("✓ All migrations applied successfully!")
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)
