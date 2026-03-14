# avaliacoes/views.py

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from services.models import Pedido
from .models import AvaliacaoCliente, AvaliacaoPrestador
from .forms import AvaliacaoClienteForm, AvaliacaoPrestadorForm


@login_required
def avaliar_como_cliente(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, cliente=request.user)

    if pedido.status != 'finalizado':
        messages.error(request, 'Só é possível avaliar pedidos finalizados.')
        return redirect('accounts:perfil')

    if hasattr(pedido, 'avaliacao_do_cliente'):
        messages.warning(request, 'Você já avaliou esse serviço.')
        return redirect('accounts:perfil')

    if request.method == 'POST':
        form = AvaliacaoClienteForm(request.POST)
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.pedido = pedido
            avaliacao.cliente = request.user
            avaliacao.prestador = pedido.servico.prestador
            avaliacao.save()
            messages.success(request, 'Avaliação enviada com sucesso! Obrigado 😊')
        else:
            messages.error(request, 'Erro ao enviar avaliação. Verifique os dados.')

    return redirect('accounts:perfil')


@login_required
def avaliar_como_prestador(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, servico__prestador=request.user)

    if pedido.status != 'finalizado':
        messages.error(request, 'Só é possível avaliar pedidos finalizados.')
        return redirect('accounts:perfil_prestador')

    if hasattr(pedido, 'avaliacao_do_prestador'):
        messages.warning(request, 'Você já avaliou esse cliente.')
        return redirect('accounts:perfil_prestador')

    if request.method == 'POST':
        form = AvaliacaoPrestadorForm(request.POST)
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.pedido = pedido
            avaliacao.prestador = request.user
            avaliacao.cliente = pedido.cliente
            avaliacao.save()
            messages.success(request, 'Avaliação enviada com sucesso!')
        else:
            messages.error(request, 'Erro ao enviar avaliação. Verifique os dados.')

    return redirect('accounts:perfil_prestador')