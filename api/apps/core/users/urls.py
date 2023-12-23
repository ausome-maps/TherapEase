from rest_framework.routers import DefaultRouter

from .api import UserViewset, ProfileViewset, OrganizationViewset

router = DefaultRouter()
router.register(r"api/list", UserViewset, basename="user-list")
router.register(r"api/profile", ProfileViewset, basename="user-profile")
router.register(r"organization", OrganizationViewset, basename="organization")

urlpatterns = []
urlpatterns += router.urls
