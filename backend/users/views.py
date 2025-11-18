import os
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import generics, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiTypes

from .serializers import (
    RegisterSerializer, UserSerializer, UserUpdateSerializer, GoogleAuthSerializer
)

User = get_user_model()

@extend_schema(tags=["Auth"], request=RegisterSerializer, responses=UserSerializer)
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

@extend_schema(tags=["Users"])
class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer           # response serializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_object(self):
        return self.request.user

    @extend_schema(responses=UserSerializer)
    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        request=UserUpdateSerializer,  # request body for PATCH
        responses=UserSerializer,      # full user in response
        examples=[
            OpenApiExample(
                "JSON update",
                value={"first_name": "Jane", "last_name": "Doe", "bio": "Afrobeats singer"},
                request_only=True,
            )
        ],
    )
    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        upd = UserUpdateSerializer(user, data=request.data, partial=True)
        upd.is_valid(raise_exception=True)
        upd.save()
        return Response(UserSerializer(user, context={"request": request}).data)

@extend_schema(
    tags=["Auth"],
    request=GoogleAuthSerializer,
    responses={200: OpenApiTypes.OBJECT, 400: OpenApiTypes.OBJECT, 500: OpenApiTypes.OBJECT},
    examples=[OpenApiExample("Google ID token", value={"id_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6Ikp..."})],
)
class GoogleAuthView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        ser = GoogleAuthSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        id_token_value = ser.validated_data["id_token"]

        client_id = os.environ.get("GOOGLE_CLIENT_ID") or getattr(settings, "GOOGLE_CLIENT_ID", None)

        # Lazy imports so server won’t crash if libs aren’t installed
        try:
            from google.oauth2 import id_token as google_id_token
            from google.auth.transport import requests as google_requests
        except Exception:
            return Response(
                {"detail": "google-auth not installed. Run: pip install google-auth google-auth-oauthlib"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Optional lazy import to avoid hard dependency at import time
        try:
            from rest_framework_simplejwt.tokens import RefreshToken
        except Exception:
            RefreshToken = None

        try:
            info = google_id_token.verify_oauth2_token(id_token_value, google_requests.Request(), client_id)
        except Exception as e:
            return Response({"detail": f"Invalid Google token: {e}"}, status=status.HTTP_400_BAD_REQUEST)

        email = info.get("email")
        first = info.get("given_name") or ""
        last = info.get("family_name") or ""
        sub = info.get("sub")

        user, _ = User.objects.get_or_create(
            email=email,
            defaults={"username": email or f"google_{sub}", "first_name": first, "last_name": last}
        )
        # keep profile fresh
        changed = False
        if first and user.first_name != first:
            user.first_name = first; changed = True
        if last and user.last_name != last:
            user.last_name = last; changed = True
        if changed:
            user.save()

        data = {"user": UserSerializer(user, context={"request": request}).data}
        if RefreshToken:
            refresh = RefreshToken.for_user(user)
            data.update({"access": str(refresh.access_token), "refresh": str(refresh)})

        return Response(data, status=200)

# Optional explicit export to avoid name confusion in imports
__all__ = ["RegisterView", "MeView", "GoogleAuthView"]