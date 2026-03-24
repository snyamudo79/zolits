from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from core.models import (
    Role,
    Region,
    Depot,
    Module,
    IssueSeverity,
    IssueStatus,
    UserProfile,
)

User = get_user_model()


class Command(BaseCommand):
    help = "Seed ZOLITS reference data and sample users"

    def add_arguments(self, parser):
        parser.add_argument("--with-sample-users", action="store_true", help="Create sample expert and regional manager users")

    def handle(self, *args, **options):
        roles = ["SUPERUSER", "USER"]
        for r in roles:
            Role.objects.get_or_create(name=r)

        # Ensure reference data for testing
        southern, _ = Region.objects.get_or_create(name="SOUTHERN", defaults={"code": "SU"})
        # Ensure code exists/updated
        if southern.code != "SU":
            southern.code = "SU"
            southern.save(update_fields=["code"])

        for depot_name in ["GWERU", "KWEKWE", "ZVISHAVANE"]:
            Depot.objects.get_or_create(region=southern, name=depot_name)

        for module_name in ["CRM", "SMART VEND", "ZUMS", "CONTRACTING", "TARIFF CHANGE", "ALL"]:
            Module.objects.get_or_create(name=module_name)

        severities = [
            ("CRITICAL", 1),
            ("HIGH", 2),
            ("MEDIUM", 3),
            ("LOW", 4),
        ]
        for name, order in severities:
            IssueSeverity.objects.get_or_create(name=name, defaults={"priority_order": order})

        statuses = [
            ("PENDING", False),
            ("ISSUE RECEIVED", False),
            ("WORK IN PROGRESS", False),
            ("NEEDS CLARIFICATION", False),
            ("RESOLVED", True),
        ]
        for name, is_resolved in statuses:
            IssueStatus.objects.get_or_create(name=name, defaults={"is_resolved_state": is_resolved})

        if options.get("with_sample_users"):
            superuser_role = Role.objects.get(name="SUPERUSER")
            user_role = Role.objects.get(name="USER")

            # user
            user, created = User.objects.get_or_create(username="user1", defaults={"email": "user1@example.com"})
            if created:
                user.set_password("Password123!")
                user.first_name = "Normal"
                user.last_name = "User"
                user.save()
            UserProfile.objects.get_or_create(user=user, defaults={"role": user_role})

            # superuser (staff)
            admin, created = User.objects.get_or_create(username="admin1", defaults={"email": "admin1@example.com"})
            if created:
                admin.set_password("Password123!")
                admin.first_name = "Admin"
                admin.last_name = "User"
                admin.is_staff = True
                admin.save()
            UserProfile.objects.get_or_create(user=admin, defaults={"role": superuser_role})

            # If a superuser exists without a profile, link as SUPERUSER
            superusers = User.objects.filter(is_superuser=True)
            for su in superusers:
                UserProfile.objects.get_or_create(user=su, defaults={"role": superuser_role})

            self.stdout.write(self.style.SUCCESS("Seeded reference data + sample users"))
        else:
            self.stdout.write(self.style.SUCCESS("Seeded reference data"))

