from django.conf import settings


class AuthDebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        if auth_header and "/users/profile/me/" in request.path:
            token = auth_header.replace("Bearer ", "")
            try:
                from rest_framework_simplejwt.settings import api_settings

                print(
                    f"DEBUG: api_settings.SIGNING_KEY={api_settings.SIGNING_KEY}",
                    flush=True,
                )
                print(f"DEBUG: settings.SECRET_KEY={settings.SECRET_KEY}", flush=True)
                print(f"DEBUG: token={token[:50]}...", flush=True)

                from rest_framework_simplejwt.backends import TokenBackend

                backend = TokenBackend(
                    algorithm="HS256", signing_key=api_settings.SIGNING_KEY
                )
                validated = backend.decode(token)
                print(f"DEBUG: validate with api_settings OK: {validated}", flush=True)
            except Exception as e:
                print(f"DEBUG: api_settings FAIL: {e}", flush=True)
                try:
                    from rest_framework_simplejwt.backends import TokenBackend

                    backend2 = TokenBackend(
                        algorithm="HS256", signing_key=settings.SECRET_KEY
                    )
                    validated2 = backend2.decode(token)
                    print(
                        f"DEBUG: validate with SECRET_KEY OK: {validated2}", flush=True
                    )
                except Exception as e2:
                    print(f"DEBUG: SECRET_KEY FAIL: {e2}", flush=True)

        response = self.get_response(request)
        return response
