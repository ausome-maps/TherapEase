from django.conf import settings
from django.http import JsonResponse

AUTH_PATH_PREFIXES = ("/auth/", "/social/")

EXEMPT_PATHS = (
    "/auth/jwt/refresh/",
    "/auth/token/logout/",
)


class AuthFeatureFlagMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not getattr(settings, "FEATURE_AUTH_ENABLED", True):
            path = request.path_info
            if path.startswith(AUTH_PATH_PREFIXES) and not path.startswith(
                EXEMPT_PATHS
            ):
                if request.method in ("POST", "PUT", "PATCH", "DELETE"):
                    return JsonResponse(
                        {"detail": "Authentication features are currently disabled."},
                        status=403,
                    )
        return self.get_response(request)
