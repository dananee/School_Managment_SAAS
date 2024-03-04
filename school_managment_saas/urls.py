"""
URL configuration for school_managment_saas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
# DRF YASG
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from school_managment.views import CurrentUserView, MyTokenObtainPairView, password_reset_confirm, activation_email_account

schema_view = get_schema_view(
    openapi.Info(
        title="Djoser API",
        default_version="v1",
        description="REST implementation of Django authentication system. djoser library provides a set of Django Rest Framework views to handle basic actions such as registration, login, logout, password reset and account activation. It works with custom user model.",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
# from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'reset-password', CustomPasswordResetConfirmView,basename="password_reset_confirm")


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(
        r"^api/v1/docs/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path('api/', include("school_managment.urls")),
    path('auth/jwt/create/', MyTokenObtainPairView.as_view(), name='customtoken'),
    path('auth/users/me/', CurrentUserView.as_view(), name='current_user'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    # path("auth/", include(router.urls)),
    path('auth/reset-password/<uidb64>/<token>',
         password_reset_confirm, name='password_reset_confirm'),
    path('auth/activate/<uidb64>/<token>',
         activation_email_account, name='activation_email_account'),

    # path('auth/blacklist/', LogoutAndBlacklistRefreshTokenForUserView.as_view(), name='blacklist')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
