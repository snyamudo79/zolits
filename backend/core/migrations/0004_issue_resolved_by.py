# Generated migration for adding resolved_by field to Issue model

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_userprofile_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='resolved_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='issues_resolved_by_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
