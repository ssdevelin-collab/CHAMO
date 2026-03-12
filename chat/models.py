# chat/models.py

from django.db import models
from django.conf import settings
from services.models import Pedido


class Conversa(models.Model):
    """Uma conversa está sempre ligada a um pedido aceito"""

    pedido = models.OneToOneField(
        Pedido,
        on_delete=models.CASCADE,
        related_name='conversa'
    )

    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='conversas_como_cliente'
    )

    prestador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='conversas_como_prestador'
    )

    criada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversa do pedido #{self.pedido.id}"


class Mensagem(models.Model):
    """Cada mensagem dentro de uma conversa"""

    conversa = models.ForeignKey(
        Conversa,
        on_delete=models.CASCADE,
        related_name='mensagens'
    )

    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mensagens_enviadas'
    )

    texto = models.TextField()
    enviada_em = models.DateTimeField(auto_now_add=True)
    lida = models.BooleanField(default=False)

    class Meta:
        ordering = ['enviada_em']  # mais antigas primeiro

    def __str__(self):
        return f"{self.autor.username}: {self.texto[:50]}"