from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # tela inicial (login)
    path('', auth_views.LoginView.as_view(
        template_name='home.html'
    ), name='home'),

    # sistema de autenticação do django
    path('accounts/', include('django.contrib.auth.urls')),

    # rotas do seu app
    path('', include('accounts.urls')),

    # serviços
    path('servicos/', include('services.urls')),
]