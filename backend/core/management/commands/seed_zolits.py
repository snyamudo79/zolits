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
        roles = ["ADMIN", "REGIONAL_MANAGER", "EXPERT", "ENDUSER"]
        for r in roles:
            Role.objects.get_or_create(name=r)

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
            admin_role = Role.objects.get(name="ADMIN")
            expert_role = Role.objects.get(name="EXPERT")
            rm_role = Role.objects.get(name="REGIONAL_MANAGER")

            # expert
            expert, created = User.objects.get_or_create(username="expert1", defaults={"email": "expert1@example.com"})
            if created:
                expert.set_password("Password123!")
                expert.first_name = "Expert"
                expert.last_name = "One"
                expert.save()
            UserProfile.objects.get_or_create(user=expert, defaults={"role": expert_role})

            # regional manager
            rm, created = User.objects.get_or_create(username="rm_southern", defaults={"email": "rm_southern@example.com"})
            if created:
                rm.set_password("Password123!")
                rm.first_name = "Regional"
                rm.last_name = "Manager"
                rm.save()
            UserProfile.objects.get_or_create(user=rm, defaults={"role": rm_role, "region": southern})

            # If a superuser exists without a profile, link as ADMIN (best-effort)
            superusers = User.objects.filter(is_superuser=True)
            for su in superusers:
                UserProfile.objects.get_or_create(user=su, defaults={"role": admin_role})

            self.stdout.write(self.style.SUCCESS("Seeded reference data + sample users"))
        else:
            self.stdout.write(self.style.SUCCESS("Seeded reference data"))

