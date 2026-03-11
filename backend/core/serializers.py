from django.utils import timezone
from rest_framework import serializers

from .models import Region, Depot, Module, IssueSeverity, IssueStatus, Issue, Attachment
from .slack import notify_new_issue


UPPERCASE_FIELDS = [
    "functionality",
    "description",
    "raised_by_name",
    "resolution_notes",
]


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ["id", "name", "code"]


class DepotSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)

    class Meta:
        model = Depot
        fields = ["id", "name", "region"]


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ["id", "name"]


class IssueSeveritySerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueSeverity
        fields = ["id", "name", "priority_order"]


class IssueStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueStatus
        fields = ["id", "name", "is_resolved_state"]


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ["id", "file", "uploaded_at"]
        read_only_fields = ["id", "uploaded_at"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")
        if request and instance.file:
            data["file"] = request.build_absolute_uri(instance.file.url)
        return data


class IssueSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Issue
        fields = [
            "id",
            "issue_number",
            "region",
            "depot",
            "module",
            "functionality",
            "description",
            "raised_by_name",
            "contact_phone",
            "issue_logged_by",
            "assigned_to",
            "severity",
            "status",
            "date_issue_raised",
            "resolution_notes",
            "zetdc_comments",
            "longshine_comments",
            "code",
            "release_date",
            "tracker",
            "issue_resolved_by",
            "date_issue_resolved",
            "attachments",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "issue_number",
            "issue_logged_by",
            "issue_resolved_by",
            "created_at",
            "updated_at",
        ]

    def _apply_uppercase(self, validated_data):
        for field in UPPERCASE_FIELDS:
            value = validated_data.get(field)
            if value:
                validated_data[field] = value.upper()

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            validated_data["issue_logged_by"] = request.user

        # set raised timestamp if not provided
        if not validated_data.get("date_issue_raised"):
            validated_data["date_issue_raised"] = timezone.now()

        # uppercase certain fields
        self._apply_uppercase(validated_data)

        # generate issue_number based on region code/prefix
        region = validated_data.get("region")
        if region:
            validated_data["issue_number"] = Issue.generate_issue_number_for_region(region)

        issue = super().create(validated_data)

        # send Slack notification to assigned expert (if any)
        if issue.assigned_to:
            notify_new_issue(issue)

        return issue

    def update(self, instance, validated_data):
        self._apply_uppercase(validated_data)

        old_status = instance.status
        issue = super().update(instance, validated_data)

        # if moved into a resolved state, record resolver and timestamp
        new_status = issue.status
        if (
            new_status
            and new_status.is_resolved_state
            and (not old_status or not old_status.is_resolved_state)
        ):
            request = self.context.get("request")
            if request and request.user and request.user.is_authenticated:
                issue.issue_resolved_by = request.user
            if not issue.date_issue_resolved:
                issue.date_issue_resolved = timezone.now()
            issue.save(update_fields=["issue_resolved_by", "date_issue_resolved"])

        # if moved out of a resolved state, clear resolver/timestamp
        if (
            old_status
            and old_status.is_resolved_state
            and (not new_status or not new_status.is_resolved_state)
        ):
            issue.issue_resolved_by = None
            issue.date_issue_resolved = None
            issue.save(update_fields=["issue_resolved_by", "date_issue_resolved"])

        return issue

