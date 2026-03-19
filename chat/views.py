# chat/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from .models import Conversa, Mensagem
from services.models import Pedido

@login_required
def api_mensagens(request, pedido_id):
    """Retorna mensagens de um pedido"""
    try:
        pedido = Pedido.objects.get(id=pedido_id)
        
        # Verificar permissão
        if request.user not in [pedido.cliente, pedido.servico.prestador]:
            return JsonResponse({'erro': 'Sem permissão'}, status=403)
        
        # Buscar ou criar conversa
        conversa, created = Conversa.objects.get_or_create(
            pedido=pedido,
            defaults={
                'cliente': pedido.cliente,
                'prestador': pedido.servico.prestador
            }
        )
        
        # Buscar mensagens
        mensagens = conversa.mensagens.select_related('autor').all()
        
        return JsonResponse({
            'conversa_id': conversa.id,
            'mensagens': [
                {
                    'texto': m.texto,
                    'autor_id': m.autor.id,
                    'autor_nome': m.autor.full_name or m.autor.username,
                    'enviada_em': m.enviada_em.strftime('%H:%M'),
                }
                for m in mensagens
            ]
        })
        
    except Pedido.DoesNotExist:
        return JsonResponse({'erro': 'Pedido não encontrado'}, status=404)


@login_required
@csrf_exempt
def enviar_mensagem(request):
    """Envia uma mensagem"""
    if request.method != 'POST':
        return JsonResponse({'erro': 'Método inválido'}, status=405)
    
    try:
        data = json.loads(request.body)
        pedido_id = data.get('pedido_id')
        texto = data.get('texto', '').strip()
        
        if not texto:
            return JsonResponse({'erro': 'Mensagem vazia'}, status=400)
        
        pedido = Pedido.objects.get(id=pedido_id)
        
        # Verificar permissão
        if request.user not in [pedido.cliente, pedido.servico.prestador]:
            return JsonResponse({'erro': 'Sem permissão'}, status=403)
        
        # Buscar conversa
        conversa = Conversa.objects.get(pedido=pedido)
        
        # Criar mensagem
        Mensagem.objects.create(
            conversa=conversa,
            autor=request.user,
            texto=texto
        )
        
        return JsonResponse({'ok': True})
        
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=400)