from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.urls import path
from django.shortcuts import render
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta, datetime
import calendar
import json

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


@admin.register(System)
class SystemAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ["name", "system"]
    list_filter = ["system"]


@admin.register(Submodule)
class SubmoduleAdmin(admin.ModelAdmin):
    list_display = ["name", "module"]
    list_filter = ["module__system", "module"]


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
    change_list_template = "admin/core/issue/change_list.html"
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
    list_filter = ["region", "system", "module", "submodule", "severity", "status", "resolved_by"]
    search_fields = ["issue_number", "description", "raised_by_name"]
    readonly_fields = [
        "issue_number",
        "date_issue_raised",
        "date_issue_resolved",
        "resolved_by",
    ]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_site.admin_view(self.dashboard_view), name='issue-dashboard'),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        local_now = timezone.localtime(timezone.now())

        # Color mapping for statuses
        status_colors = {
            'RESOLVED': '#28a745',
            'PENDING': '#dc3545',
            'WORK IN PROGRESS': '#ffc107',
            'ABORTED': '#6c757d',
            'NEW REQUIREMENTS': '#17a2b8',
            'NEEDS CLARIFICATION': '#fd7e14'
        }

        # Helper to format data for Highcharts
        def format_for_pie(queryset, label_field):
            return json.dumps([
                {
                    'name': item[label_field],
                    'y': item['count'],
                    'color': status_colors.get(item[label_field].upper(), '#36A2EB')
                } for item in queryset
            ])
        
        def format_for_column(queryset, label_field, color_key='status__name'):
            """Format data for 3D column charts with proper color mapping"""
            return json.dumps([
                {
                    'y': item['count'],
                    'color': status_colors.get(item[color_key].upper(), '#36A2EB'),
                    'name': item[label_field]
                } for item in queryset
            ])
        
        # Regional color mapping for non-status data
        region_colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#C9CBCF', '#4CAF50']

        # 1. Daily Summary
        daily_date = local_now.date() if local_now.hour >= 16 else local_now.date() - timedelta(days=1)
        daily_qs = Issue.objects.filter(date_issue_raised__date=daily_date).values('status__name').annotate(count=Count('id'))
        daily_data = format_for_pie(daily_qs, 'status__name')

        # 2. Weekly Summary
        last_friday = local_now.date() - timedelta(days=(local_now.weekday() - 4) % 7)
        weekly_date = last_friday if not (local_now.weekday() < 4 or (local_now.weekday() == 4 and local_now.hour < 16)) else last_friday - timedelta(days=7)
        week_start = weekly_date - timedelta(days=4)
        weekly_qs = Issue.objects.filter(date_issue_raised__date__range=[week_start, weekly_date]).values('status__name').annotate(count=Count('id'))
        weekly_labels = json.dumps([item['status__name'] for item in weekly_qs])
        weekly_data = format_for_column(weekly_qs, 'status__name', 'status__name')

        # 3. Monthly Summary
        last_day_of_month = calendar.monthrange(local_now.year, local_now.month)[1]
        if local_now.day == last_day_of_month and local_now.hour >= 16:
            first_day, last_day = local_now.replace(day=1), local_now.replace(day=last_day_of_month)
        else:
            first_day = (local_now.replace(day=1) - timedelta(days=1)).replace(day=1)
            last_day = local_now.replace(day=1) - timedelta(days=1)
        monthly_date = last_day
        monthly_qs = Issue.objects.filter(date_issue_raised__date__range=[first_day.date(), last_day.date()]).values('region__name').annotate(count=Count('id'))
        monthly_labels = json.dumps([q['region__name'] for q in monthly_qs])
        # Format monthly data with colors from region palette
        monthly_data_list = []
        for idx, item in enumerate(monthly_qs):
            monthly_data_list.append({
                'y': item['count'],
                'color': region_colors[idx % len(region_colors)],
                'name': item['region__name']
            })
        monthly_data = json.dumps(monthly_data_list)

        # 4. Overall System Status
        overall_qs = Issue.objects.values('status__name').annotate(count=Count('id'))
        overall_data = format_for_pie(overall_qs, 'status__name')

        context = {
            **self.admin_site.each_context(request),
            'title': 'System Activity Summary',
            'daily_date': daily_date,
            'daily_data': daily_data,
            'weekly_date': weekly_date,
            'weekly_labels': weekly_labels,
            'weekly_data': weekly_data,
            'monthly_date': monthly_date,
            'monthly_labels': monthly_labels,
            'monthly_data': monthly_data,
            'overall_data': overall_data,
        }
        return render(request, 'admin/dashboard.html', context)

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
