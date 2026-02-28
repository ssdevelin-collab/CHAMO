from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # LOGIN / LOGOUT DO DJANGO
    path('', include('django.contrib.auth.urls')),

    # SUAS ROTAS
    path('', include('accounts.urls')),
    path('servicos/', include('services.urls')),
]