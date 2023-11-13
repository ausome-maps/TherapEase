"""django_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls import static
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework import routers
from apps.core.facilities.api import FacilitiesViewset

routers = routers.SimpleRouter(trailing_slash=False)
routers.register(r"facilities", FacilitiesViewset, basename="facilities")
urlpatterns = [
    path("admin/", admin.site.urls),
    # path('accounts/', include('django.contrib.auth.urls')),
    path("users/", include("apps.core.users.urls")),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("o/", include("oauth2_provider.urls", namespace="oauth2_provider")),
]
urlpatterns += routers.urls

if settings.DEBUG:
    urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static.static(
        settings.STATIC_URL, document_root=settings.STATICFILES_DIRS
    )
