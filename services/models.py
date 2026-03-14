from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


# =========================
# SERVIÇOS DO CATÁLOGO
# =========================

class Service(models.Model):

    prestador = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='servicos'
    )

    nome = models.CharField(max_length=200)

    descricao = models.TextField()

    categoria = models.CharField(max_length=100)

    preco = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    foto = models.ImageField(
        upload_to='servicos/',
        null=True,
        blank=True
    )

    ativo = models.BooleanField(default=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - {self.prestador}"


# =========================
# PEDIDOS DOS CLIENTES
# =========================

class Pedido(models.Model):

    STATUS = (
        ('pendente', 'Pendente'),
        ('aceito', 'Aceito'),
        ('em_andamento', 'Em andamento'),
        ('finalizado', 'Finalizado'),
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

    data_inicio = models.DateTimeField(
        null=True,
        blank=True
    )

    data_finalizacao = models.DateTimeField(
        null=True,
        blank=True
    )

    observacoes = models.TextField(
        blank=True,
        null=True
    )

    endereco = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.cliente} → {self.servico}"


# =========================
# TIPOS DE PAGAMENTO
# =========================

class TipoPagamento(models.Model):

    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


# =========================
# PAGAMENTOS
# =========================

class Pagamento(models.Model):

    cliente = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE
    )

    tipo = models.ForeignKey(
        TipoPagamento,
        on_delete=models.SET_NULL,
        null=True
    )

    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ('pendente', 'Pendente'),
            ('pago', 'Pago'),
            ('cancelado', 'Cancelado')
        ],
        default='pendente'
    )

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pedido} - R$ {self.valor}"
STATUS_CHOICES = [
    ('pendente', 'Pendente'),
    ('aceito', 'Aceito'),
    ('em_andamento', 'Em andamento'),
    ('finalizado', 'Finalizado'),
]