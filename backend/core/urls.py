from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    RegionViewSet,
    DepotViewSet,
    ModuleViewSet,
    IssueSeverityViewSet,
    IssueStatusViewSet,
    IssueViewSet,
    UserViewSet,
)
from .auth_views import LoginView

router = DefaultRouter()
router.register("regions", RegionViewSet, basename="region")
router.register("depots", DepotViewSet, basename="depot")
router.register("modules", ModuleViewSet, basename="module")
router.register("severities", IssueSeverityViewSet, basename="severity")
router.register("statuses", IssueStatusViewSet, basename="status")
router.register("issues", IssueViewSet, basename="issue")
router.register("users", UserViewSet, basename="user")

urlpatterns = [
    path("auth/login/", LoginView.as_view(), name="api-login"),
    path("", include(router.urls)),
]

