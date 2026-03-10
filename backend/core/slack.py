import os
from typing import Optional

import requests

from .models import Issue, UserProfile


SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN", "")
SLACK_API_URL = "https://slack.com/api/chat.postMessage"


def _get_slack_user_id_for_django_user(user) -> Optional[str]:
    if not user:
        return None
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        return None
    return profile.slack_user_id or None


def _post_to_slack(slack_user_id: str, text: str) -> None:
    if not SLACK_BOT_TOKEN or not slack_user_id:
        return
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json; charset=utf-8",
    }
    payload = {
        "channel": slack_user_id,
        "text": text,
    }
    try:
        requests.post(SLACK_API_URL, headers=headers, json=payload, timeout=5)
    except Exception:
        # Fail silently in app; logging can be added later
        pass


def notify_new_issue(issue: Issue) -> None:
    slack_user_id = _get_slack_user_id_for_django_user(issue.assigned_to)
    if not slack_user_id:
        return

    severity = issue.severity.name.upper() if issue.severity else ""
    status = issue.status.name.upper() if issue.status else ""
    text = (
        f"HEY {issue.assigned_to.get_full_name() or issue.assigned_to.username}, "
        f"YOU HAVE A NEW {severity} ISSUE {issue.issue_number} "
        f"WITH STATUS {status} IN REGION {issue.region.name.upper()}."
    )
    _post_to_slack(slack_user_id, text)


def notify_critical_issue_reminder(issue: Issue) -> None:
    slack_user_id = _get_slack_user_id_for_django_user(issue.assigned_to)
    if not slack_user_id:
        return

    status = issue.status.name.upper() if issue.status else ""
    text = (
        f"REMINDER: YOU HAVE AN OPEN CRITICAL ISSUE {issue.issue_number} "
        f"– CURRENT STATUS: {status}."
    )
    _post_to_slack(slack_user_id, text)

