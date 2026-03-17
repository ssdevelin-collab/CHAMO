from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Conversa, Mensagem


@login_required
def chat_view(request, pedido_id):

    conversa = get_object_or_404(Conversa, pedido_id=pedido_id)

    mensagens = conversa.mensagens.all().order_by('criada_em')

    if request.method == 'POST':

        texto = request.POST.get('mensagem')

        if texto:
            Mensagem.objects.create(
                conversa=conversa,
                remetente=request.user,
                texto=texto
            )

        return redirect('chat:chat', pedido_id=pedido_id)

    return render(
        request,
        'chat/chat.html',
        {
            'conversa': conversa,
            'mensagens': mensagens
        }
    )