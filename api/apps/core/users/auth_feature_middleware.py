from django.conf import settings
from django.http import JsonResponse

AUTH_PATH_PREFIXES = ("/auth/", "/social/")

EXEMPT_PATHS = (
    "/auth/jwt/refresh/",
    "/auth/token/logout/",
)

# Exact paths to block when FEATURE_REGISTRATION_ENABLED is 0 (POST only)
REGISTRATION_BLOCKED_EXACT = (
    "/auth/users/",  # Djoser user create (registration)
    "/users/social/jwt/",  # social auth JWT endpoint
)

SOCIAL_AUTH_PATH_PREFIXES = ("/social/",)


class AuthFeatureFlagMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info

        if not getattr(settings, "FEATURE_AUTH_ENABLED", True):
            if path.startswith(AUTH_PATH_PREFIXES) and not path.startswith(
                EXEMPT_PATHS
            ):
                if request.method in ("POST", "PUT", "PATCH", "DELETE"):
                    return JsonResponse(
                        {"detail": "Authentication features are currently disabled."},
                        status=403,
                    )

        if not getattr(settings, "FEATURE_REGISTRATION_ENABLED", True):
            if request.method in ("POST", "PUT", "PATCH", "DELETE"):
                if path in REGISTRATION_BLOCKED_EXACT or path.startswith(
                    SOCIAL_AUTH_PATH_PREFIXES
                ):
                    return JsonResponse(
                        {
                            "detail": "Registration and social authentication are currently disabled. Existing users may still log in."
                        },
                        status=403,
                    )

        return self.get_response(request)
