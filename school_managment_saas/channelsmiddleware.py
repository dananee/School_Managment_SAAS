from channels.auth import AuthMiddlewareStack
from rest_framework import Token
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware


class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        jwt_auth = JWTAuthentication()
        headers = dict(scope['headers'])
        if b'authorization' in headers:
            try:
                user, _ = await database_sync_to_async(jwt_auth.authenticate)(request=None)
                scope['user'] = user if user else AnonymousUser()
            except Exception as e:
                scope['user'] = AnonymousUser()
        return await super().__call__(scope, receive, send)

TokenAuthMiddlewareStack = lambda inner: JWTAuthMiddleware(AuthMiddlewareStack(inner))