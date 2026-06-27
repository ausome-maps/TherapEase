from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_tracking.mixins import LoggingMixin
from .models import Profile, Organization
from .serializers import (
    ProfileSerializer,
    OrganizationSerializer,
)
from .permissions import OrganizationPermissions


class ProfileViewset(LoggingMixin, viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfileSerializer

    def initial(self, request, *args, **kwargs):
        import sys

        print(
            f"DEBUG_INITIAL: auth={request.META.get('HTTP_AUTHORIZATION', 'NONE')[:50]}",
            file=sys.stderr,
            flush=True,
        )
        from rest_framework_simplejwt.settings import api_settings

        print(
            f"DEBUG_INITIAL: sign_key={api_settings.SIGNING_KEY[:15]} algo={api_settings.ALGORITHM}",
            file=sys.stderr,
            flush=True,
        )
        try:
            from rest_framework_simplejwt.tokens import AccessToken

            t = request.META.get("HTTP_AUTHORIZATION", "").replace("Bearer ", "")
            if t:
                tok = AccessToken(t)
                print(
                    f"DEBUG_INITIAL: manual_decode=OK user_id={tok.get('user_id')}",
                    file=sys.stderr,
                    flush=True,
                )
        except Exception as e:
            print(f"DEBUG_INITIAL: manual_decode=FAIL {e}", file=sys.stderr, flush=True)
        return super().initial(request, *args, **kwargs)

    def should_log(self, request, response):
        """Log only errors"""
        return response.status_code >= 400

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    @action(detail=False, methods=["get", "patch"], name="me")
    def me(self, request):
        import sys
        from django.conf import settings as dj_settings

        print(
            f"DEBUG_ME: auth_header={request.META.get('HTTP_AUTHORIZATION', 'NONE')[:80]}",
            file=sys.stderr,
            flush=True,
        )
        print(
            f"DEBUG_ME: secret_key={dj_settings.SECRET_KEY[:10]}... sign_key={dj_settings.SIMPLE_JWT.get('SIGNING_KEY', 'NOT SET')[:10]}...",
            file=sys.stderr,
            flush=True,
        )
        try:
            from rest_framework_simplejwt.tokens import AccessToken

            t = request.META.get("HTTP_AUTHORIZATION", "").replace("Bearer ", "")
            token = AccessToken(t)
            print(
                f"DEBUG_ME: token_valid=True user_id={token.get('user_id')}",
                file=sys.stderr,
                flush=True,
            )
        except Exception as e:
            print(f"DEBUG_ME: token_valid=False error={e}", file=sys.stderr, flush=True)

        profile = self.get_queryset().first()
        if not profile:
            return Response(
                {"detail": "Profile not found"}, status=status.HTTP_404_NOT_FOUND
            )
        if request.method == "GET":
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        elif request.method == "PATCH":
            serializer = self.get_serializer(profile, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data)


class OrganizationViewset(LoggingMixin, viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    permission_classes = (OrganizationPermissions,)
    serializer_class = OrganizationSerializer
