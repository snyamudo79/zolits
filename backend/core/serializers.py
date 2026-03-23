import re
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Region, Depot, System, Module, Submodule, IssueSeverity, IssueStatus, Issue, Attachment, Role, UserProfile
from .slack import notify_new_issue

User = get_user_model()


UPPERCASE_FIELDS = [
    "description",
    "raised_by_name",
    "resolution_notes",
]


class SystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = System
        fields = ["id", "name"]


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
    system = SystemSerializer(read_only=True)

    class Meta:
        model = Module
        fields = ["id", "name", "system"]


class SubmoduleSerializer(serializers.ModelSerializer):
    module = ModuleSerializer(read_only=True)

    class Meta:
        model = Submodule
        fields = ["id", "name", "module"]


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
            "system",
            "module",
            "submodule",
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
            "resolved_by",
            "date_issue_resolved",
            "attachments",
            "screenshot",
        ]
        read_only_fields = [
            "id",
            "issue_number",
            "issue_logged_by",
            "resolved_by",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['region'] = RegionSerializer(instance.region).data if instance.region else None
        representation['depot'] = DepotSerializer(instance.depot).data if instance.depot else None
        representation['system'] = SystemSerializer(instance.system).data if instance.system else None
        representation['module'] = ModuleSerializer(instance.module).data if instance.module else None
        representation['submodule'] = SubmoduleSerializer(instance.submodule).data if instance.submodule else None
        representation['severity'] = IssueSeveritySerializer(instance.severity).data if instance.severity else None
        representation['status'] = IssueStatusSerializer(instance.status).data if instance.status else None
        representation['issue_logged_by'] = instance.issue_logged_by.get_full_name() or instance.issue_logged_by.username
        if instance.assigned_to:
            representation['assigned_to'] = instance.assigned_to.get_full_name() or instance.assigned_to.username
        if instance.resolved_by:
            representation['resolved_by'] = instance.resolved_by.get_full_name() or instance.resolved_by.username
        return representation

    def _apply_uppercase(self, validated_data):
        for field in UPPERCASE_FIELDS:
            value = validated_data.get(field)
            if value:
                validated_data[field] = value.upper()

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            validated_data["issue_logged_by"] = request.user
        else:
            # Fallback for AllowAny unauthenticated requests
            from django.contrib.auth import get_user_model
            User = get_user_model()
            default_user = User.objects.first()
            if default_user:
                validated_data["issue_logged_by"] = default_user

        # set raised timestamp if not provided
        if not validated_data.get("date_issue_raised"):
            validated_data["date_issue_raised"] = timezone.now()

        # uppercase certain fields
        self._apply_uppercase(validated_data)

        # generate issue_number based on region code/prefix
        region = validated_data.get("region")
        if region:
            validated_data["issue_number"] = Issue.generate_issue_number_for_region(region)

        # Set default status to 'PENDING'
        pending_status, _ = IssueStatus.objects.get_or_create(name="PENDING")
        validated_data["status"] = pending_status

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
                issue.resolved_by = request.user
            if not issue.date_issue_resolved:
                issue.date_issue_resolved = timezone.now()
            issue.save(update_fields=["resolved_by", "date_issue_resolved"])

        # if moved out of a resolved state, clear resolver/timestamp
        if (
            old_status
            and old_status.is_resolved_state
            and (not new_status or not new_status.is_resolved_state)
        ):
            issue.resolved_by = None
            issue.date_issue_resolved = None
            issue.save(update_fields=["resolved_by", "date_issue_resolved"])

        return issue


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), required=False)
    region = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all(), required=False)

    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "last_name", "role", "region"]

    def validate_email(self, value):
        if not value.endswith("@zetdc.co.zw"):
            raise serializers.ValidationError("Email must belong to the domain @zetdc.co.zw")
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_username(self, value):
        # normalize username by adding prefix if missing
        username = value.lower()
        if not username.startswith("ze"):
            username = f"ze{username}"
        
        # validate it is ze followed by digits
        if not re.match(r"^ze\d+$", username):
            raise serializers.ValidationError("Username must start with 'ze' followed by digits.")
        
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        
        return username

    def create(self, validated_data):
        role = validated_data.pop("role", None)
        region = validated_data.pop("region", None)
        
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        # Create profile
        if not role:
            # default to ENDUSER
            role, _ = Role.objects.get_or_create(name="ENDUSER")
        
        UserProfile.objects.create(user=user, role=role, region=region)
        
        return user
