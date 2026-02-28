from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [

    path('', views.lista_servicos, name='lista_servicos'),
    path('criar/', views.criar_servico, name='criar_servico'),
    path('editar/<int:id>/', views.editar_servico, name='editar_servico'),
    path('excluir/<int:id>/', views.excluir_servico, name='excluir_servico'),
    path(
        'contratar/<int:servico_id>/',
        views.contratar_servico,
        name='contratar_servico'
    ),

    path(
        'meus-pedidos/',
        views.meus_pedidos,
        name='meus_pedidos'
    ),

  
    path(
        'pedidos/',
        views.pedidos_prestador,
        name='pedidos_prestador'
    ),

    path(
        'aceitar/<int:pedido_id>/',
        views.aceitar_pedido,
        name='aceitar_pedido'
    ),

    path(
        'recusar/<int:pedido_id>/',
        views.recusar_pedido,
        name='recusar_pedido'
    ),
]