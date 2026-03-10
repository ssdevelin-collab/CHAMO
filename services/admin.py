from django.contrib import admin
from .models import Service, Pedido
from .models import Service, Pedido, TipoPagamento, Pagamento

admin.site.register(Service)
admin.site.register(Pedido)
admin.site.register(TipoPagamento)
admin.site.register(Pagamento)