from django.core.management.base import BaseCommand

from core.models import Issue
from core.slack import notify_critical_issue_reminder


class Command(BaseCommand):
    help = "Send Slack reminders for unresolved critical issues"

    def handle(self, *args, **options):
        qs = Issue.objects.filter(
            severity__name__iexact="CRITICAL",
            status__is_resolved_state=False,
        ).select_related("assigned_to", "severity", "status", "region")

        count = 0
        for issue in qs:
            if issue.assigned_to:
                notify_critical_issue_reminder(issue)
                count += 1

        self.stdout.write(self.style.SUCCESS(f"Sent reminders for {count} critical issues"))

