from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import login
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {"access": str(refresh.access_token), "refresh": str(refresh)}


@api_view(["POST"])
@permission_classes([AllowAny])
def social_auth_jwt(request):
    provider = request.data.get("provider")
    access_token = request.data.get("access_token")

    if not provider or not access_token:
        return JsonResponse(
            {"detail": "provider and access_token are required"}, status=400
        )

    try:
        if provider == "google-oauth2":
            from social_core.backends.google import GoogleOAuth2

            backend = GoogleOAuth2()
        elif provider == "facebook":
            from social_core.backends.facebook import FacebookOAuth2

            backend = FacebookOAuth2()
        else:
            return JsonResponse({"detail": "unsupported provider"}, status=400)

        user = backend.do_auth(access_token)
        if user and user.is_active:
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            tokens = get_tokens_for_user(user)
            return JsonResponse(tokens)
        return JsonResponse({"detail": "authentication failed"}, status=400)
    except Exception as e:
        return JsonResponse({"detail": str(e)}, status=400)


def social_auth_complete_redirect(request):
    if not request.user or not request.user.is_authenticated:
        return HttpResponseRedirect(
            f"{settings.SITE_URL}/login?error=social_auth_failed"
        )

    tokens = get_tokens_for_user(request.user)
    return HttpResponseRedirect(
        f"{settings.SITE_URL}/?access={tokens['access']}&refresh={tokens['refresh']}"
    )
