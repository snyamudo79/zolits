from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

class ExpiringTokenAuthentication(TokenAuthentication):
    """
    Custom token authentication that expires tokens after 30 minutes.
    """
    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise AuthenticationFailed('User inactive or deleted')

        # Check if token has expired (30 minutes)
        # We use token.created to check the age of the token.
        # Note: If you want tokens to expire 30 minutes after LAST USE, 
        # you would need to update a 'last_used' field on every request.
        # For simplicity, we'll implement 30 minutes since CREATION.
        
        utc_now = timezone.now()
        if token.created < utc_now - timedelta(minutes=30):
            # Delete expired token so the user has to log in again
            token.delete()
            raise AuthenticationFailed('Token has expired')

        return (token.user, token)
