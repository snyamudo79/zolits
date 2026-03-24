from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import (
    Role,
    Region,
    Depot,
    System,
    Module,
    Submodule,
    IssueSeverity,
    IssueStatus,
    UserProfile,
    Issue,
    Attachment,
    IssueHistory,
)

User = get_user_model()


@admin.register(System)
class SystemAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Submodule)
class SubmoduleAdmin(admin.ModelAdmin):
    list_display = ["name", "module"]
    list_filter = ["module"]


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
        "system",
        "module",
        "submodule",
        "severity",
        "status",
        "assigned_to",
        "date_issue_raised",
        "date_issue_resolved",
        "resolved_by",
    ]
    list_filter = ["region", "system", "module", "severity", "status", "resolved_by"]
    search_fields = ["issue_number", "description", "raised_by_name"]
    readonly_fields = [
        "issue_number",
        "date_issue_raised",
        "date_issue_resolved",
        "resolved_by",
        "created_at",
        "updated_at",
    ]

    def save_model(self, request, obj, form, change):
        """
        When updating via admin, automatically set resolved_by if status changed to resolved.
        """
        if change:
            old_obj = Issue.objects.get(pk=obj.pk)
            if (
                obj.status
                and obj.status.is_resolved_state
                and (not old_obj.status or not old_obj.status.is_resolved_state)
            ):
                obj.resolved_by = request.user
                from django.utils import timezone
                if not obj.date_issue_resolved:
                    obj.date_issue_resolved = timezone.now()
            elif (
                old_obj.status
                and old_obj.status.is_resolved_state
                and (not obj.status or not obj.status.is_resolved_state)
            ):
                obj.resolved_by = None
                obj.date_issue_resolved = None
        
        super().save_model(request, obj, form, change)
    inlines = [AttachmentInline, IssueHistoryInline]


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ["issue", "file", "uploaded_by", "uploaded_at"]


@admin.register(IssueHistory)
class IssueHistoryAdmin(admin.ModelAdmin):
    list_display = ["issue", "changed_by", "changed_at", "field_name"]
    list_filter = ["field_name"]
    readonly_fields = ["issue", "changed_by", "changed_at", "field_name", "old_value", "new_value"]
