from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('<int:pedido_id>/', views.chat_view, name='chat'),
]