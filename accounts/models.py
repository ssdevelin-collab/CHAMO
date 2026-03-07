from django.contrib.auth.models import AbstractUser
from django.db import models


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

    full_name = models.CharField(max_length=255, null=True, blank=True)
    cpf = models.CharField(max_length=14, unique=True, null=True, blank=True)
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)

    birth_date = models.DateField(null=True, blank=True)

    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.username


class PrestadorProfile(models.Model):

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil_prestador'
    )

    nome_empresa = models.CharField(max_length=200)

    descricao = models.TextField()

    categoria = models.CharField(max_length=100)

    cidade = models.CharField(max_length=100)

    foto = models.ImageField(
        upload_to='prestadores/',
        blank=True,
        null=True
    )

    ativo = models.BooleanField(default=True)

    # localização (para mapa ou busca por proximidade)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome_empresa


class Avaliacao(models.Model):

    prestador = models.ForeignKey(
        PrestadorProfile,
        on_delete=models.CASCADE,
        related_name='avaliacoes'
    )

    cliente = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    nota = models.IntegerField()

    comentario = models.TextField(blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avaliação {self.nota}⭐ para {self.prestador.nome_empresa}"