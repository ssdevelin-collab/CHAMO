from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [

    path(
        '',
        views.lista_servicos,
        name='lista_servicos'
    ),

    path(
        'criar/',
        views.criar_servico,
        name='criar_servico'
    ),

    path(
        'editar/<int:servico_id>/',
        views.editar_servico,
        name='editar_servico'
    ),

    path(
        'excluir/<int:servico_id>/',
        views.excluir_servico,
        name='excluir_servico'
    ),

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
        'andamento/',
        views.servicos_andamento,
        name='servicos_andamento'
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

    path(
        'iniciar/<int:pedido_id>/',
        views.iniciar_servico,
        name='iniciar_servico'
    ),

    path(
        'finalizar/<int:pedido_id>/',
        views.finalizar_servico,
        name='finalizar_servico'
    ),

    path(
        'mapa/',
        views.buscar_prestadores,
        name='buscar_prestadores'
    ),

    path(
        'api/prestadores/',
        views.api_prestadores_proximos,
        name='api_prestadores'
    ),

    path(
        'meu-catalogo/',
        views.catalogo_prestador,
        name='catalogo_prestador'
    ),
    path(
    'api/buscar-servicos/',
    views.buscar_servicos_api,
    name='buscar_servicos_api'
    ),
        path(
        'meu-catalogo/',
        views.catalogo_prestador,
        name='catalogo_prestador'
    ),

    path(
        'api/buscar-servicos/',
        views.buscar_servicos_api,
        name='buscar_servicos_api'
    ),

    path(
        'prestador/<int:user_id>/',
        views.pagina_prestador,
        name='pagina_prestador'
    ),
]