"""
ASGI config for thu_lost_and_found_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""
from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()

import os
import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from thu_lost_and_found_backend.chat_service import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'thu_lost_and_found_backend.settings')
django.setup()


application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})