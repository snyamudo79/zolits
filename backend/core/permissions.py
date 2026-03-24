from rest_framework import permissions

class IsSuperUserOrUser(permissions.BasePermission):
    """
    Custom permission to only allow SUPERUSER to have full access,
    and USER to have limited reporting access.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        # Superusers (Django is_superuser or Role='SUPERUSER')
        try:
            role_name = request.user.profile.role.name
        except AttributeError:
            role_name = None

        if request.user.is_superuser or role_name == 'SUPERUSER':
            return True

        # Normal USER role
        if role_name == 'USER':
            # Block USER from seeing other users entirely
            if view.__class__.__name__ == 'UserViewSet':
                return False

            # USER can report (POST) and view (GET) their own issues
            if view.__class__.__name__ == 'IssueViewSet':
                return request.method in ['POST', 'GET']
            
            # USER can read reference data (Regions, Modules, etc.)
            if request.method in permissions.SAFE_METHODS:
                return True
            
        return False

    def has_object_permission(self, request, view, obj):
        # Superusers can do anything
        try:
            role_name = request.user.profile.role.name
        except AttributeError:
            role_name = None

        if request.user.is_superuser or role_name == 'SUPERUSER':
            return True
            
        # USER can only see their own issues
        if role_name == 'USER' and view.__class__.__name__ == 'IssueViewSet':
             return obj.issue_logged_by == request.user
             
        return False
