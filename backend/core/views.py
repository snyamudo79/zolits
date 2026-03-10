from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Region, Depot, Module, IssueSeverity, IssueStatus, Issue, Attachment
from .serializers import (
    RegionSerializer,
    DepotSerializer,
    ModuleSerializer,
    IssueSeveritySerializer,
    IssueStatusSerializer,
    IssueSerializer,
    AttachmentSerializer,
)

User = get_user_model()


class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [permissions.IsAuthenticated]


class DepotViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Depot.objects.select_related("region").all()
    serializer_class = DepotSerializer
    permission_classes = [permissions.IsAuthenticated]


class ModuleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [permissions.IsAuthenticated]


class IssueSeverityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = IssueSeverity.objects.all()
    serializer_class = IssueSeveritySerializer
    permission_classes = [permissions.IsAuthenticated]


class IssueStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = IssueStatus.objects.all()
    serializer_class = IssueStatusSerializer
    permission_classes = [permissions.IsAuthenticated]


class IssueViewSet(viewsets.ModelViewSet):
    queryset = (
        Issue.objects.select_related(
            "region",
            "depot",
            "module",
            "severity",
            "status",
            "assigned_to",
            "issue_logged_by",
            "issue_resolved_by",
        )
        .prefetch_related("attachments")
        .all()
    )
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """
        Return enriched list suitable for dashboards and colored table:
        includes region/module/severity/status names, resolved flag,
        resolver, dates, description, resolution and screenshot info.
        """
        queryset = self.get_queryset()
        data = []
        for issue in queryset:
            resolved_by_name = (
                issue.issue_resolved_by.get_full_name()
                or issue.issue_resolved_by.username
                if issue.issue_resolved_by
                else ""
            )
            logged_by_name = (
                issue.issue_logged_by.get_full_name()
                or issue.issue_logged_by.username
                if issue.issue_logged_by
                else ""
            )
            attachments = issue.attachments.all()
            data.append(
                {
                    "id": issue.id,
                    "issue_number": issue.issue_number,
                    "region_name": issue.region.name,
                    "depot_name": issue.depot.name,
                    "module_name": issue.module.name,
                    "severity_name": issue.severity.name,
                    "status_name": issue.status.name,
                    "status_is_resolved_state": issue.status.is_resolved_state,
                    "date_issue_raised": issue.date_issue_raised,
                    "date_issue_resolved": issue.date_issue_resolved,
                    "description": issue.description,
                    "resolution_notes": issue.resolution_notes,
                    "resolved_by_name": resolved_by_name,
                    "issue_logged_by_name": logged_by_name,
                    "attachments": [
                        {"id": a.id, "file": request.build_absolute_uri(a.file.url), "uploaded_at": a.uploaded_at}
                        for a in attachments
                    ],
                }
            )
        return Response(data)

    @action(detail=True, methods=["post"], url_path="attachments")
    def upload_attachment(self, request, pk=None):
        issue = self.get_object()
        file = request.FILES.get("file")
        if not file:
            return Response({"detail": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        attachment = Attachment.objects.create(issue=issue, file=file, uploaded_by=request.user)
        serializer = AttachmentSerializer(attachment, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="resolve")
    def resolve(self, request, pk=None):
        """
        Convenience endpoint for experts: set status to a resolved state and set resolution notes.
        Body: { "status": <status_id>, "resolution_notes": "..." }
        """
        issue = self.get_object()
        status_id = request.data.get("status")
        if not status_id:
            return Response({"detail": "status is required"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(issue, data={"status": status_id, "resolution_notes": request.data.get("resolution_notes", "")}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Very small user listing endpoint for assigning experts.
    In a real deployment you'd probably filter by role.
    """

    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        users = self.get_queryset()
        data = [
            {
                "id": u.id,
                "username": u.username,
                "full_name": u.get_full_name(),
            }
            for u in users
        ]
        return Response(data)

