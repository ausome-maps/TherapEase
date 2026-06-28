import json
from urllib.request import Request, urlopen
from urllib.error import URLError
from urllib.parse import urlencode
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.conf import settings

PUBLIC_NOMINATIM = "https://nominatim.openstreetmap.org/search"


def _fetch_nominatim(base_url: str, q: str):
    params = urlencode({
        "q": q + ", Philippines",
        "format": "json",
        "limit": 5,
        "countrycodes": "ph",
    })
    req = Request(
        f"{base_url}?{params}",
        headers={"User-Agent": f"TherapEase/{settings.SITE_NAME}"},
    )
    with urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode())


@require_GET
def geocode_view(request):
    q = request.GET.get("q", "").strip()
    if not q:
        return JsonResponse({"error": "Missing query parameter 'q'"}, status=400)

    configured_url = settings.GEOCODE_URL.rstrip("/")
    urls_to_try = [configured_url]
    if configured_url != PUBLIC_NOMINATIM:
        urls_to_try.append(PUBLIC_NOMINATIM)

    last_error = None
    for base_url in urls_to_try:
        try:
            data = _fetch_nominatim(base_url, q)
            features = []
            for r in data:
                features.append({
                    "display_name": r.get("display_name", ""),
                    "lat": r.get("lat"),
                    "lon": r.get("lon"),
                })
            return JsonResponse({"features": features, "total": len(features)})
        except URLError as e:
            last_error = e
            continue

    return JsonResponse(
        {"error": f"Geocoding service unavailable: {last_error.reason if last_error else 'unknown'}"},
        status=503,
    )
