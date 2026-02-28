from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


# ======================
# SERVICE
# ======================
class Service(models.Model):

    prestador = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='servicos'
    )

    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    categoria = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=8, decimal_places=2)

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


# ======================
# PEDIDO
# ======================
class Pedido(models.Model):

    STATUS = (
        ('pendente', 'Pendente'),
        ('aceito', 'Aceito'),
        ('recusado', 'Recusado'),
    )

    cliente = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='pedidos_cliente'
    )

    servico = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='pedidos'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='pendente'
    )

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cliente} → {self.servico}"