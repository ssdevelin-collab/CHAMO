from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from services.models import Pedido
from .models import Conversa, Mensagem
 
 
@login_required
def abrir_chat(request, pedido_id):
    """
    Abre ou cria uma conversa para um pedido aceito.
    Só funciona se o pedido estiver com status 'aceito' ou posterior.
    """
    pedido = get_object_or_404(Pedido, id=pedido_id)
 
    # Verifica se o usuário é o cliente ou prestador do pedido
    prestador = pedido.servico.prestador
    cliente = pedido.cliente
 
    if request.user not in [cliente, prestador]:
        messages.error(request, 'Você não tem acesso a esse chat.')
        return redirect('home')
 
    # Só permite chat após o pedido ser aceito
    if pedido.status not in ['aceito', 'em_andamento', 'finalizado']:
        messages.error(request, 'O chat só fica disponível após o pedido ser aceito.')
        return redirect('home')
 
    # Cria a conversa se ainda não existir
    conversa, _ = Conversa.objects.get_or_create(
        pedido=pedido,
        defaults={'cliente': cliente, 'prestador': prestador}
    )
 
    # Busca histórico de mensagens
    mensagens = conversa.mensagens.select_related('autor').all()
 
    return render(request, 'chat/chat.html', {
        'conversa': conversa,
        'mensagens': mensagens,
        'pedido': pedido,
    })