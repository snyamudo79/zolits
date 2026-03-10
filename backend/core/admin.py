from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import (
    Role,
    Region,
    Depot,
    Module,
    IssueSeverity,
    IssueStatus,
    UserProfile,
    Issue,
    Attachment,
    IssueHistory,
)

User = get_user_model()


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ["name", "code"]


@admin.register(Depot)
class DepotAdmin(admin.ModelAdmin):
    list_display = ["name", "region"]
    list_filter = ["region"]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(IssueSeverity)
class IssueSeverityAdmin(admin.ModelAdmin):
    list_display = ["name", "priority_order"]
    ordering = ["priority_order", "name"]


@admin.register(IssueStatus)
class IssueStatusAdmin(admin.ModelAdmin):
    list_display = ["name", "is_resolved_state"]


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    extra = 0


try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "role", "region", "slack_user_id"]
    list_filter = ["role", "region"]
    search_fields = ["user__username", "user__email"]


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 0
    readonly_fields = ["uploaded_at"]


class IssueHistoryInline(admin.TabularInline):
    model = IssueHistory
    extra = 0
    readonly_fields = ["changed_by", "changed_at", "field_name", "old_value", "new_value"]
    can_delete = False
    max_num = 20


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = [
        "issue_number",
        "region",
        "depot",
        "module",
        "severity",
        "status",
        "assigned_to",
        "date_issue_raised",
        "date_issue_resolved",
    ]
    list_filter = ["region", "severity", "status"]
    search_fields = ["issue_number", "description", "raised_by_name"]
    readonly_fields = ["issue_number", "date_issue_raised", "date_issue_resolved", "created_at", "updated_at"]
    inlines = [AttachmentInline, IssueHistoryInline]


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ["issue", "file", "uploaded_by", "uploaded_at"]


@admin.register(IssueHistory)
class IssueHistoryAdmin(admin.ModelAdmin):
    list_display = ["issue", "changed_by", "changed_at", "field_name"]
    list_filter = ["field_name"]
    readonly_fields = ["issue", "changed_by", "changed_at", "field_name", "old_value", "new_value"]
