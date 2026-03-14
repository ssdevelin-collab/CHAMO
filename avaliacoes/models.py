# avaliacoes/models.py

from django.db import models
from django.conf import settings
from services.models import Pedido


NOTAS = [
    (1, '1 - Péssimo'),
    (2, '2 - Ruim'),
    (3, '3 - Regular'),
    (4, '4 - Bom'),
    (5, '5 - Excelente'),
]


class AvaliacaoCliente(models.Model):
    """Cliente avalia o prestador após o serviço finalizado"""

    pedido = models.OneToOneField(
        Pedido,
        on_delete=models.CASCADE,
        related_name='avaliacao_do_cliente'
    )
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='avaliacoes_feitas'
    )
    prestador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='avaliacoes_recebidas'
    )
    nota = models.IntegerField(choices=NOTAS)
    comentario = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return f"{self.cliente.username} avaliou {self.prestador.username} — nota {self.nota}"


class AvaliacaoPrestador(models.Model):
    """Prestador avalia o cliente após o serviço finalizado"""

    pedido = models.OneToOneField(
        Pedido,
        on_delete=models.CASCADE,
        related_name='avaliacao_do_prestador'
    )
    prestador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='avaliacoes_dadas'
    )
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='avaliacoes_recebidas_como_cliente'
    )
    nota = models.IntegerField(choices=NOTAS)
    comentario = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return f"{self.prestador.username} avaliou {self.cliente.username} — nota {self.nota}"