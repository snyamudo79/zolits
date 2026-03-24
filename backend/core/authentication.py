from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')

        # Token expiration check (10 minutes)
        utc_now = timezone.now()
        if token.created < utc_now - timedelta(minutes=10):
            token.delete()
            raise exceptions.AuthenticationFailed('Token has expired. Please login again.')

        return (token.user, token)
