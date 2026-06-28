from rest_framework.routers import SimpleRouter

from .api import FacilitySubmissionViewset

router = SimpleRouter(trailing_slash=False)
router.register(r"", FacilitySubmissionViewset, basename="submissions")
urlpatterns = []
urlpatterns += router.urls
