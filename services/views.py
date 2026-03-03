from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ServiceForm
from django.db.models import Q
from .models import Service, Pedido
from .forms import PedidoForm
from .models import Pedido
import json
import math
from django.http import JsonResponse
from accounts.models import PrestadorProfile


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

    if request.user.user_type != 'prestador':
        return redirect('accounts:dashboard')

    pedidos = Pedido.objects.filter(
        servico__prestador=request.user,
        status='pendente'
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

<<<<<<< HEAD
@login_required
def iniciar_servico(request, pedido_id):

    pedido = get_object_or_404(Pedido, id=pedido_id)

    if pedido.servico.prestador != request.user:
        return redirect('accounts:dashboard')

    pedido.status = 'em_andamento'
    pedido.save()

    return redirect('services:pedidos_prestador')


@login_required
def finalizar_servico(request, pedido_id):

    pedido = get_object_or_404(Pedido, id=pedido_id)

    if pedido.servico.prestador != request.user:
        return redirect('accounts:dashboard')

    pedido.status = 'finalizado'
    pedido.save()

    return redirect('services:pedidos_prestador')

def pedidos_recebidos(request):

    pedidos = Pedido.objects.filter(
        servico__prestador=request.user
    ).order_by('-criado_em')

    return render(request, 'services/pedidos_recebidos.html', {
        'pedidos': pedidos
    })

@login_required
def servicos_andamento(request):

    if request.user.user_type != 'prestador':
        return redirect('accounts:dashboard')

    pedidos = Pedido.objects.filter(
        servico__prestador=request.user,
        status__in=['aceito', 'em_andamento']
    )

    return render(
        request,
        'services/servicos_andamento.html',
        {'pedidos': pedidos}
    )
@login_required
def servicos_andamento(request):

    if request.user.user_type != 'prestador':
        return redirect('accounts:dashboard')

    pedidos = Pedido.objects.filter(
        servico__prestador=request.user,
        status__in=['aceito', 'em_andamento']
    ).order_by('-criado_em')

    return render(
        request,
        'services/servicos_andamento.html',
        {'pedidos': pedidos}
    )
=======
def calcular_distancia(lat1, lon1, lat2, lon2) -> float:
    """
    Fórmula de Haversine — calcula distância em km entre dois pontos geográficos.
    """
    R = 6371  # raio da Terra em km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    return R * 2 * math.asin(math.sqrt(a))


@login_required
def buscar_prestadores(request):
    """
    View principal — renderiza o mapa com a lista de prestadores.
    """
    return render(request, 'busca/mapa_prestadores.html')


@login_required
def api_prestadores_proximos(request):
    """
    Endpoint JSON chamado pelo JavaScript do mapa.
    Recebe: lat, lng, raio (em km)
    Retorna: lista de prestadores dentro do raio
    """
    try:
        lat_cliente = float(request.GET.get('lat'))
        lng_cliente = float(request.GET.get('lng'))
        raio_km     = float(request.GET.get('raio', 5))  # padrão: 5km
    except (TypeError, ValueError):
        return JsonResponse({'erro': 'Parâmetros inválidos.'}, status=400)

    # Busca todos os prestadores ativos com coordenadas cadastradas
    prestadores = PrestadorProfile.objects.filter(
        ativo=True,
        latitude__isnull=False,
        longitude__isnull=False
    ).select_related('usuario')

    resultado = []
    for p in prestadores:
        distancia = calcular_distancia(lat_cliente, lng_cliente, p.latitude, p.longitude)

        if distancia <= raio_km:
            resultado.append({
                'id':          p.id,
                'nome':        p.nome_empresa,
                'categoria':   p.categoria,
                'cidade':      p.cidade,
                'descricao':   p.descricao[:100] + '...' if len(p.descricao) > 100 else p.descricao,
                'distancia':   round(distancia, 2),
                'lat':         p.latitude,
                'lng':         p.longitude,
                'foto':        p.foto.url if p.foto else None,
            })

    # Ordena do mais próximo ao mais distante
    resultado.sort(key=lambda x: x['distancia'])

    return JsonResponse({'prestadores': resultado})
>>>>>>> origin/Lorena
