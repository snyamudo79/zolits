from django.contrib.auth import authenticate
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer


class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            
            return Response(
                {
                    "token": token.key,
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "full_name": user.get_full_name(),
                        "role": user.profile.role.name if hasattr(user, 'profile') else None,
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    authentication_classes = []  # disable auth for login
    permission_classes = []

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user=user)
        
        # If token exists but is older than 10 minutes, regenerate it
        from django.utils import timezone
        from datetime import timedelta
        if not created and token.created < timezone.now() - timedelta(minutes=10):
            token.delete()
            token = Token.objects.create(user=user)

        return Response(
            {
                "token": token.key,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "full_name": user.get_full_name(),
                    "role": user.profile.role.name if hasattr(user, 'profile') else None,
                },
            }
        )


class MeView(APIView):
    """
    Returns the current user's profile and role based on the HTTP-only cookie.
    If the user is not authenticated, returns a 200 OK with authenticated: false.
    This prevents scary 401 errors in the frontend console on initial load.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"authenticated": False}, status=status.HTTP_200_OK)

        user = request.user
        return Response({
            "authenticated": True,
            "id": user.id,
            "username": user.username,
            "full_name": user.get_full_name(),
            "role": user.profile.role.name if hasattr(user, 'profile') else None,
        })


class LogoutView(APIView):
    """
    Clears the HTTP-only auth cookie and deletes the token from the database.
    """
    def post(self, request):
        response = Response({"detail": "Successfully logged out"}, status=status.HTTP_200_OK)
        
        # Delete token from database if it exists
        if request.user.is_authenticated:
            Token.objects.filter(user=request.user).delete()

        # Clear the cookie
        response.delete_cookie('auth_token', path='/')
        return response

