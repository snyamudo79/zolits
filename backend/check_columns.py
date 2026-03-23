from django.db import connection
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zolits_backend.settings')
django.setup()

with connection.cursor() as cursor:
    cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'core_issue' ORDER BY ordinal_position")
    print([row[0] for row in cursor.fetchall()])
