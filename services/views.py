from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.models import User

import math

from .forms import ServiceForm
from .models import Service, Pedido
from accounts.models import PrestadorProfile


# =========================
# CALCULAR DISTÂNCIA
# =========================

def calcular_distancia(lat1, lng1, lat2, lng2):
    R = 6371

    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)

    a = (
        math.sin(dlat/2)**2 +
        math.cos(math.radians(lat1)) *
        math.cos(math.radians(lat2)) *
        math.sin(dlng/2)**2
    )

    return R * 2 * math.asin(math.sqrt(a))


# =========================
# CRIAR SERVIÇO
# =========================

@login_required
def criar_servico(request):

    if request.user.user_type != 'prestador':
        return redirect('accounts:dashboard')

    if request.method == 'POST':

        form = ServiceForm(request.POST)

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


# =========================
# EDITAR SERVIÇO
# =========================

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


# =========================
# EXCLUIR SERVIÇO
# =========================

@login_required
def excluir_servico(request, id):

    servico = get_object_or_404(
        Service,
        id=id,
        prestador=request.user
    )

    servico.delete()

    return redirect('accounts:dashboard_prestador')


# =========================
# LISTAR SERVIÇOS
# =========================

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

    return render(
        request,
        'services/lista_servicos.html',
        {'servicos': servicos}
    )


# =========================
# CONTRATAR SERVIÇO
# =========================

@login_required
def contratar_servico(request, servico_id):

    if request.user.user_type != 'cliente':
        return redirect('accounts:dashboard')

    servico = get_object_or_404(
        Service,
        id=servico_id
    )

    Pedido.objects.create(
        cliente=request.user,
        servico=servico,
        status='pendente'
    )

    return redirect('services:meus_pedidos')


# =========================
# MEUS PEDIDOS
# =========================

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


# =========================
# PEDIDOS PRESTADOR
# =========================
# =========================
# ACEITAR PEDIDO
# =========================

@login_required
def aceitar_pedido(request, pedido_id):

    pedido = get_object_or_404(
        Pedido,
        id=pedido_id
    )

    if pedido.servico.prestador != request.user:
        return redirect('accounts:dashboard')

    pedido.status = 'aceito'
    pedido.save()

    return redirect('accounts:dashboard_prestador')


# =========================
# RECUSAR PEDIDO
# =========================

@login_required
def recusar_pedido(request, pedido_id):

    pedido = get_object_or_404(
        Pedido,
        id=pedido_id
    )

    if pedido.servico.prestador != request.user:
        return redirect('accounts:dashboard')

    pedido.status = 'recusado'
    pedido.save()

    return redirect('accounts:dashboard_prestador')


# =========================
# INICIAR SERVIÇO
# =========================

@login_required
def iniciar_servico(request, pedido_id):

    pedido = get_object_or_404(
        Pedido,
        id=pedido_id
    )

    if pedido.servico.prestador != request.user:
        return redirect('accounts:dashboard')

    pedido.status = 'em_andamento'
    pedido.data_inicio = timezone.now()

    pedido.save()

    return redirect('accounts:dashboard_prestador')


# =========================
# FINALIZAR SERVIÇO
# =========================

@login_required
def finalizar_servico(request, pedido_id):

    pedido = get_object_or_404(
        Pedido,
        id=pedido_id
    )

    if pedido.servico.prestador != request.user:
        return redirect('accounts:dashboard')

    pedido.status = 'finalizado'
    pedido.data_finalizacao = timezone.now()

    pedido.save()

    return redirect('accounts:dashboard_prestador')


# =========================
# SERVIÇOS EM ANDAMENTO
# =========================

@login_required
def servicos_andamento(request):

    pedidos = Pedido.objects.filter(
        servico__prestador=request.user,
        status='em_andamento'
    ).order_by('-criado_em')

    return render(
        request,
        'services/servicos_andamento.html',
        {'pedidos': pedidos}
    )


# =========================
# MAPA DE PRESTADORES
# =========================

@login_required
def buscar_prestadores(request):

    return render(
        request,
        'busca/mapa_prestadores.html'
    )


# =========================
# API PRESTADORES PRÓXIMOS
# =========================

@login_required
def api_prestadores_proximos(request):

    try:

        lat = float(request.GET.get('lat'))
        lng = float(request.GET.get('lng'))
        raio = float(request.GET.get('raio', 5))

    except (TypeError, ValueError):

        return JsonResponse(
            {'erro': 'Parâmetros inválidos.'},
            status=400
        )

    grau_lat = raio / 111.0
    grau_lng = raio / (111.0 * math.cos(math.radians(lat)))

    prestadores = PrestadorProfile.objects.filter(
        ativo=True,
        latitude__isnull=False,
        longitude__isnull=False,
        latitude__range=(lat - grau_lat, lat + grau_lat),
        longitude__range=(lng - grau_lng, lng + grau_lng),
    )

    resultado = []

    for p in prestadores:

        distancia = calcular_distancia(
            lat,
            lng,
            p.latitude,
            p.longitude
        )

        if distancia <= raio:

            resultado.append({
                'nome': p.nome_empresa,
                'categoria': p.categoria,
                'descricao': p.descricao,
                'cidade': p.cidade,
                'lat': p.latitude,
                'lng': p.longitude,
                'distancia': round(distancia, 1),
            })

    resultado.sort(key=lambda x: x['distancia'])

    return JsonResponse({'prestadores': resultado})


# =========================
# CATÁLOGO DO PRESTADOR
# =========================

@login_required
def catalogo_prestador(request):

    servicos = Service.objects.filter(
        prestador=request.user
    )

    return render(
        request,
        'services/catalogo_prestador.html',
        {'servicos': servicos}
    )


# =========================
# API BUSCAR SERVIÇOS
# =========================

@login_required
def buscar_servicos_api(request):

    termo = request.GET.get('q')

    if not termo:
        return JsonResponse({'servicos': []})

    servicos = Service.objects.filter(
        Q(nome__icontains=termo) |
        Q(categoria__icontains=termo)
    )[:10]

    resultado = []

    for s in servicos:

        resultado.append({

            'id': s.id,
            'nome': s.nome,
            'categoria': s.categoria,

            'prestador': s.prestador.username,
            'prestador_id': s.prestador.id,

            'preco': float(s.preco)

        })

    return JsonResponse({'servicos': resultado})


# =========================
# PÁGINA DO PRESTADOR
# =========================

@login_required
def pagina_prestador(request, user_id):

    prestador = get_object_or_404(
        User,
        id=user_id
    )

    servicos = Service.objects.filter(
        prestador=prestador,
        ativo=True
    )

    return render(
        request,
        'services/pagina_prestador.html',
        {
            'prestador': prestador,
            'servicos': servicos
        }
    )
@login_required
def pedidos_prestador(request):

    pedidos_pendentes = Pedido.objects.filter(
        servico__prestador=request.user,
        status='pendente'
    )

    pedidos_andamento = Pedido.objects.filter(
        servico__prestador=request.user,
        status__in=['aceito', 'em_andamento']
    )

    pedidos_finalizados = Pedido.objects.filter(
        servico__prestador=request.user,
        status='finalizado'
    )

    return render(
        request,
        'services/pedidos_prestador.html',
        {
            'pedidos_pendentes': pedidos_pendentes,
            'pedidos_andamento': pedidos_andamento,
            'pedidos_finalizados': pedidos_finalizados
        }
    )