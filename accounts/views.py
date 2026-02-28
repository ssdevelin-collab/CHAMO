from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, PrestadorProfileForm
from .models import PrestadorProfile
from services.models import Service


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
            form.save()
            return redirect('login')

    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


# ===============================
# DASHBOARD PRINCIPAL
# ===============================
@login_required
def dashboard(request):

    # se for prestador → vai pro painel dele
    if request.user.user_type == 'prestador':
        return redirect('accounts:dashboard_prestador')

    # se for cliente
    return redirect('accounts:dashboard_cliente')


# ===============================
# DASHBOARD CLIENTE
# ===============================
@login_required
def dashboard_cliente(request):
    return render(
        request,
        'accounts/dashboard_cliente.html'
    )


# ===============================
# DASHBOARD PRESTADOR
# ===============================
@login_required
def dashboard_prestador(request):

    # bloqueia cliente
    if request.user.user_type != 'prestador':
        return redirect('accounts:dashboard')

    servicos = Service.objects.filter(
        prestador=request.user
    )

    return render(
        request,
        'accounts/dashboard_prestador.html',
        {'servicos': servicos}
    )


# ===============================
# PERFIL DO PRESTADOR
# ===============================
@login_required
def perfil_prestador(request):

    # bloqueia cliente
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