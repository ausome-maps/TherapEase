from django.urls import path
from rest_framework.routers import DefaultRouter

from .api import UserViewset, RegisterView, ProfileViewset
from .views import *

router = DefaultRouter()
router.register(r"api/list", UserViewset, basename="user-list")
router.register(r"api/profile", ProfileViewset, basename="user-profile")

urlpatterns = []
urlpatterns += router.urls
