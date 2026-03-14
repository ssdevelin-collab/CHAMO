from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


# =========================
# USUÁRIO CUSTOMIZADO
# =========================

class User(AbstractUser):

    USER_TYPES = (
        ('cliente', 'Cliente'),
        ('prestador', 'Prestador'),
    )

    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPES,
        default='cliente'
    )

    full_name = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    cpf = models.CharField(
        max_length=14,
        unique=True,
        null=True,
        blank=True
    )

    phone = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True
    )

    birth_date = models.DateField(
        null=True,
        blank=True
    )

    address = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    city = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.username


# =========================
# PERFIL DO PRESTADOR
# =========================

class PrestadorProfile(models.Model):

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfil_prestador'
    )

        
    foto = models.ImageField(
    upload_to='perfil/',
    null=True,
    blank=True
    )

    nome_empresa = models.CharField(
        max_length=200,
        blank=True
    )

    descricao = models.TextField(
        blank=True
    )

    categoria = models.CharField(
        max_length=100,
        blank=True
    )

    cidade = models.CharField(
        max_length=100,
        blank=True
    )

    ativo = models.BooleanField(default=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.usuario.username



# =========================
# AVALIAÇÃO DE PRESTADOR
# =========================

class Avaliacao(models.Model):

    prestador = models.ForeignKey(
        PrestadorProfile,
        on_delete=models.CASCADE,
        related_name='avaliacoes'
    )

    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    nota = models.IntegerField()

    comentario = models.TextField(blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nota}⭐ para {self.prestador.usuario.username}"
class ClienteProfile(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfil_cliente'
    )
    foto = models.ImageField(upload_to='perfil/', null=True, blank=True)

    def __str__(self):
        return self.usuario.username
