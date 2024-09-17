"""
URL configuration for school_managment_saas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Classe-based views
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
 

from school_managment.views import (
    CurrentUserView,
    HomePage,
  
    MeetingPage,
    MyTokenObtainPairView,
    password_reset_confirm,
    activation_email_account,
    reset_password_page,
)

 
# from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'reset-password', CustomPasswordResetConfirmView,basename="password_reset_confirm")
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("", HomePage.as_view()),
    path("meeting/", MeetingPage.as_view()),
    path("admin/", admin.site.urls),
      

   
    path("api/", include("school_managment.urls")),
    path("auth/jwt/create/", MyTokenObtainPairView.as_view(), name="customtoken"),
    path("auth/users/me/", CurrentUserView.as_view(), name="current_user"),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    # path("auth/", include(router.urls)),
    path(
        "auth/reset-password/<uidb64>/<token>",
        reset_password_page,
        name="password_reset_confirm",
    ),
    path(
        "auth/activate/<uidb64>/<token>",
        activation_email_account,
        name="activation_email_account",
    ),
    # path('auth/blacklist/', LogoutAndBlacklistRefreshTokenForUserView.as_view(), name='blacklist')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path("", HomePage.as_view(), name="home_page"),
)


from school_managment.consumer import NotificationConsumer

websocket_urlpatterns = [
    path("ws/notifications/<str:role>/", NotificationConsumer.as_asgi())
]
