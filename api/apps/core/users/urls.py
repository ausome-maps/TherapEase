from rest_framework.routers import DefaultRouter

from .api import ProfileViewset, OrganizationViewset

router = DefaultRouter()
router.register(r"api/profile", ProfileViewset, basename="user-profile")
router.register(r"organization", OrganizationViewset, basename="organization")

urlpatterns = []
urlpatterns = urlpatterns + router.urls
