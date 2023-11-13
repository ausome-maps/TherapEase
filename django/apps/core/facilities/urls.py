from django.urls import path
from rest_framework.routers import SimpleRouter

from .api import FacilitiesViewset

router = SimpleRouter(trailing_slash=False)
router.register(r"", FacilitiesViewset, basename="facilities-list")
urlpatterns = [
    path(
        "api/search",
        FacilitiesViewset.as_view({"get": "search"}),
        name="facilities-search",
    ),
]

urlpatterns = urlpatterns + router.urls
