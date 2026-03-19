from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('chat/api/mensagens/<int:pedido_id>/', views.api_mensagens, name='api_mensagens'),
    path('chat/enviar/', views.enviar_mensagem, name='enviar_mensagem'),
]