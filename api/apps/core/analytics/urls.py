from django.urls import path
from rest_framework.routers import SimpleRouter

from .api import (
    AnalyticsViewset,
    PageVisitViewset,
    FacilityViewViewset,
    SearchQueryViewset,
)

router = SimpleRouter(trailing_slash=False)
router.register(r"page-visits", PageVisitViewset, basename="analytics-page-visits")
router.register(r"facility-views", FacilityViewViewset, basename="analytics-facility-views")
router.register(r"search-queries", SearchQueryViewset, basename="analytics-search-queries")

urlpatterns = [
    path(
        "track/page-visit",
        AnalyticsViewset.as_view({"post": "track_page_visit"}),
        name="analytics-track-page-visit",
    ),
    path(
        "track/facility-view",
        AnalyticsViewset.as_view({"post": "track_facility_view"}),
        name="analytics-track-facility-view",
    ),
    path(
        "track/search-query",
        AnalyticsViewset.as_view({"post": "track_search_query"}),
        name="analytics-track-search-query",
    ),
    path(
        "cleanup-bots",
        AnalyticsViewset.as_view({"post": "cleanup_bots"}),
        name="analytics-cleanup-bots",
    ),
]

urlpatterns += router.urls
