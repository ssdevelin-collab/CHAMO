# Rotas do WebSocket (equivalente ao urls.py, mas para WebSocket)
 
from django.urls import re_path
from . import consumers
 
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<conversa_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]
 