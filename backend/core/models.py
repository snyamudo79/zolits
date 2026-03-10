from django.conf import settings
from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)  # e.g. "SU" for Southern

    def __str__(self) -> str:
        return self.name


class Depot(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="depots")
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ("region", "name")

    def __str__(self) -> str:
        return f"{self.name} ({self.region.code})"


class Module(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class IssueSeverity(models.Model):
    name = models.CharField(max_length=50, unique=True)
    priority_order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["priority_order", "name"]

    def __str__(self) -> str:
        return self.name


class IssueStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_resolved_state = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    slack_user_id = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:
        return f"{self.user.get_full_name()} ({self.role.name})"


class Issue(models.Model):
    issue_number = models.CharField(max_length=20, unique=True)
    region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name="issues")
    depot = models.ForeignKey(Depot, on_delete=models.PROTECT, related_name="issues")
    module = models.ForeignKey(Module, on_delete=models.PROTECT, related_name="issues")

    functionality = models.CharField(max_length=255)
    description = models.TextField()

    raised_by_name = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=50, blank=True)

    issue_logged_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="issues_logged",
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="issues_assigned",
    )

    severity = models.ForeignKey(IssueSeverity, on_delete=models.PROTECT)
    status = models.ForeignKey(IssueStatus, on_delete=models.PROTECT)

    date_issue_raised = models.DateTimeField()

    resolution_notes = models.TextField(blank=True)
    zetdc_comments = models.TextField(blank=True)
    longshine_comments = models.TextField(blank=True)
    code = models.CharField(max_length=100, blank=True)
    release_date = models.DateField(null=True, blank=True)
    tracker = models.CharField(max_length=100, blank=True)

    issue_resolved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="issues_resolved",
    )
    date_issue_resolved = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_issue_raised"]

    def __str__(self) -> str:
        return self.issue_number

    @staticmethod
    def generate_issue_number_for_region(region: Region) -> str:
        """
        Generate the next issue number for a given region, following the pattern
        like SU32, SU101, etc., where Region.code is the prefix (e.g. "SU").
        """
        prefix = (region.code or "").upper()
        if not prefix:
            raise ValueError("Region.code must be set to generate issue number")

        last_issue = (
            Issue.objects.filter(issue_number__startswith=prefix)
            .order_by("-id")
            .first()
        )
        if last_issue and last_issue.issue_number[len(prefix) :].isdigit():
            last_number = int(last_issue.issue_number[len(prefix) :])
        else:
            last_number = 0

        next_number = last_number + 1
        return f"{prefix}{next_number}"


class Attachment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField(upload_to="attachments/")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)


class IssueHistory(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="history")
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    field_name = models.CharField(max_length=100)
    old_value = models.TextField(blank=True)
    new_value = models.TextField(blank=True)

    class Meta:
        ordering = ["-changed_at"]

