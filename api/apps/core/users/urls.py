from django.urls import path
from rest_framework.routers import DefaultRouter

from .api import ProfileViewset, OrganizationViewset
from .social import social_auth_jwt, social_auth_complete_redirect

router = DefaultRouter()
router.register(r"profile", ProfileViewset, basename="user-profile")
router.register(r"organization", OrganizationViewset, basename="organization")

urlpatterns = [
    path("social/jwt/", social_auth_jwt, name="social-auth-jwt"),
    path("social/complete/", social_auth_complete_redirect, name="social-auth-complete"),
]
urlpatterns = urlpatterns + router.urls
