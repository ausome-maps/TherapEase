from rest_framework.routers import SimpleRouter

from .api import FeedbackViewset

router = SimpleRouter(trailing_slash=False)
router.register(r"", FeedbackViewset, basename="feedback")
urlpatterns = []
urlpatterns += router.urls
