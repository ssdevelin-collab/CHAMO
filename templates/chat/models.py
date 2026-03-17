from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Conversa(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversas_cliente')
    prestador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversas_prestador')
    pedido = models.OneToOneField('services.Pedido', on_delete=models.CASCADE)

    criada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cliente} x {self.prestador}"


class Mensagem(models.Model):
    conversa = models.ForeignKey(Conversa, on_delete=models.CASCADE, related_name='mensagens')
    remetente = models.ForeignKey(User, on_delete=models.CASCADE)

    texto = models.TextField()

    criada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.remetente}: {self.texto[:20]}"