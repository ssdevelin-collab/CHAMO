from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('admin/', admin.site.urls),

    # tela inicial (login)
    path('', auth_views.LoginView.as_view(
        template_name='home.html'
    ), name='home'),

    # sistema de autenticação do django
    path('accounts/', include('django.contrib.auth.urls')),

    # rotas do app accounts
    path('', include('accounts.urls')),

    # serviços
    path('servicos/', include('services.urls')),

    # chat
    path('', include('chat.urls')),
]


# SERVIR ARQUIVOS DE MEDIA (FOTOS DE PERFIL)

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )