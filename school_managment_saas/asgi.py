"""
ASGI config for school_managment_saas project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
# from .channelsmiddleware import JWTAuthMiddleware


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_managment_saas.settings")

from . import urls

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": URLRouter(urls.websocket_urlpatterns),
    }
)
