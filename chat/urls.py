# chat/urls.py

from django.urls import path
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from . import views
from .models import Conversa


@login_required
def historico(request, conversa_id):
    """Endpoint que retorna o histórico de mensagens em JSON"""
    try:
        conversa = Conversa.objects.get(id=conversa_id)
        if request.user not in [conversa.cliente, conversa.prestador]:
            return JsonResponse({'erro': 'Sem permissão'}, status=403)

        mensagens = conversa.mensagens.select_related('autor').all()
        return JsonResponse({
            'mensagens': [
                {
                    'texto': m.texto,
                    'autor_id': m.autor.id,
                    'autor_nome': m.autor.username,
                    'enviada_em': m.enviada_em.strftime('%H:%M'),
                }
                for m in mensagens
            ]
        })
    except Conversa.DoesNotExist:
        return JsonResponse({'mensagens': []})


urlpatterns = [
    path('chat/<int:pedido_id>/', views.abrir_chat, name='abrir_chat'),
    path('chat/historico/<int:conversa_id>/', historico, name='chat_historico'),
]