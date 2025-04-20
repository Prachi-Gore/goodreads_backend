import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "goodreads_backend.settings")
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.middleware import TokenAuthMiddleware
import chat.routing



application = ProtocolTypeRouter({
    "http": get_asgi_application(),  
    "websocket": TokenAuthMiddleware(
        AuthMiddlewareStack(
            URLRouter(
                chat.routing.websocket_urlpatterns
            )
        )
    ),
})
