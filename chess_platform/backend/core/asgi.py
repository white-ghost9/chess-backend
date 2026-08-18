import os
import django
from django.core.asgi import get_asgi_application

# 1. Set settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# 2. Initialize Django ASGI application FIRST
django_asgi_app = get_asgi_application()

# 3. NOW import routing / channels stuff (after django setup)
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chess_game.routing

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack(
            URLRouter(chess_game.routing.websocket_urlpatterns)
        ),
    }
)
