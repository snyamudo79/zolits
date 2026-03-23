import os
import django

# SET SETTINGS FIRST
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zolits_backend.settings')
django.setup()

from django.utils import timezone
from datetime import timedelta
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()

def test_token_expiration():
    # 1. Create a user
    user, _ = User.objects.get_or_create(username='test_auth_user')
    user.set_password('testpass123')
    user.save()

    # 2. Create an expired token (40 minutes ago)
    Token.objects.filter(user=user).delete()
    token = Token.objects.create(user=user)
    # Since Token.created is auto_now_add, we need to update it manually via .filter().update()
    Token.objects.filter(key=token.key).update(created=timezone.now() - timedelta(minutes=40))
    token.refresh_from_db()
    
    print(f"Created expired token for user {user.username}: {token.key}")

    # 3. Try to authenticate with the expired token
    from core.authentication import ExpiringTokenAuthentication
    from rest_framework.exceptions import AuthenticationFailed

    auth = ExpiringTokenAuthentication()
    try:
        auth.authenticate_credentials(token.key)
        print("FAILED: Authenticated with expired token!")
    except AuthenticationFailed as e:
        print(f"SUCCESS: Authentication failed as expected: {str(e)}")

    # 4. Create a valid token (5 minutes ago)
    Token.objects.filter(user=user).delete()
    token = Token.objects.create(user=user)
    Token.objects.filter(key=token.key).update(created=timezone.now() - timedelta(minutes=5))
    token.refresh_from_db()

    try:
        user_authenticated, token_authenticated = auth.authenticate_credentials(token.key)
        print(f"SUCCESS: Authenticated with valid token for user {user_authenticated.username}")
    except AuthenticationFailed as e:
        print(f"FAILED: Authentication failed for valid token: {str(e)}")

if __name__ == "__main__":
    test_token_expiration()
