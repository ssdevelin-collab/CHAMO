from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ServiceForm
from django.db.models import Q
from .models import Service, Pedido
from .forms import PedidoForm
from django.contrib.auth.decorators import login_required
from .models import Pedido

@login_required
def criar_servico(request):


    if request.user.user_type != 'prestador':
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)

        if form.is_valid():
            servico = form.save(commit=False)
            servico.prestador = request.user
            servico.save()

           
            return redirect('accounts:dashboard_prestador')

    else:
        form = ServiceForm()

    return render(
        request,
        'services/criar_servico.html',
        {'form': form}
    )


@login_required
def editar_servico(request, id):

    servico = get_object_or_404(
        Service,
        id=id,
        prestador=request.user
    )

    if request.method == 'POST':
        form = ServiceForm(
            request.POST,
            request.FILES,
            instance=servico
        )

        if form.is_valid():
            form.save()
            return redirect('accounts:dashboard_prestador')

    else:
        form = ServiceForm(instance=servico)

    return render(
        request,
        'services/criar_servico.html',
        {'form': form}
    )


@login_required
def excluir_servico(request, id):

    servico = get_object_or_404(
        Service,
        id=id,
        prestador=request.user
    )

    servico.delete()

    return redirect('accounts:dashboard_prestador')



def lista_servicos(request):

    busca = request.GET.get('busca')
    cidade = request.GET.get('cidade')

    servicos = Service.objects.all()

  
    if busca:
        servicos = servicos.filter(
            Q(nome__icontains=busca) |
            Q(descricao__icontains=busca)
        )

    if cidade:
        servicos = servicos.filter(
            prestador__city__icontains=cidade
        )

    context = {
        'servicos': servicos
    }

    return render(
        request,
        'services/lista_servicos.html',
        context
    )



@login_required
def contratar_servico(request, servico_id):

    if request.user.user_type != 'cliente':
        return redirect('accounts:dashboard')

    servico = Service.objects.get(id=servico_id)

    Pedido.objects.create(
        cliente=request.user,
        servico=servico
    )

    return redirect('services:meus_pedidos')

@login_required
def meus_pedidos(request):

    pedidos = Pedido.objects.filter(
        cliente=request.user
    )

    return render(
        request,
        'services/meus_pedidos.html',
        {'pedidos': pedidos}
    )



@login_required
def pedidos_prestador(request):

    print("USUÁRIO LOGADO:", request.user)
    print("TIPO:", request.user.user_type)

    pedidos = Pedido.objects.all()

    for p in pedidos:
        print(
            p.id,
            p.servico.nome,
            p.servico.prestador
        )

    pedidos = Pedido.objects.filter(
        servico__prestador_id=request.user.id
    )

    return render(
        request,
        'services/pedidos_prestador.html',
        {'pedidos': pedidos}
    )

@login_required
def aceitar_pedido(request, pedido_id):

    pedido = get_object_or_404(Pedido, id=pedido_id)

    if pedido.servico.prestador != request.user:
        return redirect('accounts:dashboard')

    pedido.status = 'aceito'
    pedido.save()

    return redirect('services:pedidos_prestador')

@login_required
def recusar_pedido(request, pedido_id):

    pedido = get_object_or_404(Pedido, id=pedido_id)

    if pedido.servico.prestador != request.user:
        return redirect('accounts:dashboard')

    pedido.status = 'recusado'
    pedido.save()

    return redirect('services:pedidos_prestador')