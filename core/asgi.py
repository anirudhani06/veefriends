"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.urls import path
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.consumers import GroupConsumer, ChatConsumer
from posts.consumers import NotificationConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

websocket_urlpatterns = [
    path("ws/chat/<str:room>/", GroupConsumer.as_asgi()),
    path("ws/message/<str:username>/", ChatConsumer.as_asgi()),
    path("ws/activity/<str:username>/", NotificationConsumer.as_asgi()),
]

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)
