from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

from .forms import RegisterForm, PrestadorProfileForm
from .models import PrestadorProfile
from services.models import Service, Pedido


# ===============================
# HOME
# ===============================

def home(request):
    return render(request, 'home.html')


# ===============================
# REGISTRO
# ===============================

def register(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            # cria perfil automaticamente se for prestador
            if user.user_type == 'prestador':
                PrestadorProfile.objects.create(usuario=user)

            login(request, user)

            return redirect('accounts:dashboard')

    else:
        form = RegisterForm()

    return render(
        request,
        'register.html',
        {'form': form}
    )


# ===============================
# REDIRECIONAMENTO DE DASHBOARD
# ===============================

@login_required
def dashboard(request):

    if request.user.user_type == 'prestador':
        return redirect('accounts:dashboard_prestador')

    return redirect('accounts:dashboard_cliente')


# ===============================
# DASHBOARD CLIENTE
# ===============================

@login_required
def dashboard_cliente(request):

    pedidos = Pedido.objects.filter(
        cliente=request.user
    ).order_by('-criado_em')

    context = {
        'pedidos': pedidos
    }

    return render(
        request,
        'accounts/dashboard_cliente.html',
        context
    )


# ===============================
# DASHBOARD PRESTADOR
# ===============================

@login_required
def dashboard_prestador(request):

    # serviços do prestador
    servicos = Service.objects.filter(
        prestador=request.user
    )

    # pedidos aguardando resposta
    pedidos_pendentes = Pedido.objects.filter(
        servico__prestador=request.user,
        status='pendente'
    )

    # serviços ativos (aceito + em andamento)
    pedidos_andamento = Pedido.objects.filter(
        servico__prestador=request.user,
        status__in=['aceito', 'em_andamento']
    )

    # serviços finalizados
    pedidos_finalizados = Pedido.objects.filter(
        servico__prestador=request.user,
        status='finalizado'
    )

    context = {
        'servicos': servicos,
        'pedidos_pendentes': pedidos_pendentes,
        'pedidos_andamento': pedidos_andamento,
        'pedidos_finalizados': pedidos_finalizados,
    }

    return render(
        request,
        'accounts/dashboard_prestador.html',
        context
    )


# ===============================
# PERFIL DO PRESTADOR
# ===============================

@login_required
def perfil_prestador(request):

    # impede cliente de acessar
    if request.user.user_type != 'prestador':
        return redirect('accounts:dashboard')

    perfil, created = PrestadorProfile.objects.get_or_create(
        usuario=request.user
    )

    if request.method == 'POST':

        form = PrestadorProfileForm(
            request.POST,
            request.FILES,
            instance=perfil
        )

        if form.is_valid():
            form.save()
            return redirect('accounts:dashboard_prestador')

    else:
        form = PrestadorProfileForm(instance=perfil)

    return render(
        request,
        'accounts/perfil_prestador.html',
        {'form': form}
    )