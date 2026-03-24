from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    RegionViewSet,
    DepotViewSet,
    SystemViewSet,
    ModuleViewSet,
    SubmoduleViewSet,
    IssueSeverityViewSet,
    IssueStatusViewSet,
    IssueViewSet,
    UserViewSet,
)
from .auth_views import LoginView, RegisterView, MeView, LogoutView

router = DefaultRouter()
router.register("regions", RegionViewSet, basename="region")
router.register("depots", DepotViewSet, basename="depot")
router.register("systems", SystemViewSet, basename="system")
router.register("modules", ModuleViewSet, basename="module")
router.register("submodules", SubmoduleViewSet, basename="submodule")
router.register("severities", IssueSeverityViewSet, basename="severity")
router.register("statuses", IssueStatusViewSet, basename="status")
router.register("issues", IssueViewSet, basename="issue")
router.register("users", UserViewSet, basename="user")

urlpatterns = [
    path("auth/login/", LoginView.as_view(), name="api-login"),
    path("auth/register/", RegisterView.as_view(), name="api-register"),
    path("auth/me/", MeView.as_view(), name="api-me"),
    path("auth/logout/", LogoutView.as_view(), name="api-logout"),
    
    # Also support paths without trailing slashes for frontend convenience
    path("auth/login", LoginView.as_view()),
    path("auth/register", RegisterView.as_view()),
    path("auth/me", MeView.as_view()),
    path("auth/logout", LogoutView.as_view()),

    path("", include(router.urls)),
]

