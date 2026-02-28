from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, PrestadorProfileForm
from .models import PrestadorProfile
from services.models import Service
from services.models import Service, Pedido



def home(request):
    return render(request, 'home.html')


def register(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


@login_required
def dashboard(request):

  
    if request.user.user_type == 'prestador':
        return redirect('accounts:dashboard_prestador')

   
    return redirect('accounts:dashboard_cliente')


@login_required
def dashboard_cliente(request):
    return render(
        request,
        'accounts/dashboard_cliente.html'
    )


@login_required
def dashboard_prestador(request):

    servicos = Service.objects.filter(
        prestador=request.user
    )

    pedidos_pendentes = Pedido.objects.filter(
        servico__prestador=request.user,
        status='pendente'
    )

    pedidos_andamento = Pedido.objects.filter(
        servico__prestador=request.user,
        status__in=['aceito', 'em_andamento']
    )

    context = {
        'servicos': servicos,
        'pedidos_pendentes': pedidos_pendentes,
        'pedidos_andamento': pedidos_andamento,
    }

    return render(
        request,
        'accounts/dashboard_prestador.html',
        context
    )


@login_required
def perfil_prestador(request):


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