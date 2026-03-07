from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # HOME = tela inicial/login customizado
    path('', auth_views.LoginView.as_view(
        template_name='home.html'
    ), name='home'),

    # rotas do sistema de login do django
    path('accounts/', include('django.contrib.auth.urls')),

    # rotas do seu app accounts (register, dashboard etc)
    path('', include('accounts.urls')),

    # serviços
    path('servicos/', include('services.urls')),
]