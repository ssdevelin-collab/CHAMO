# accounts/signals.py
# Sempre que um PrestadorProfile for salvo, geocodifica o endereço automaticamente

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PrestadorProfile
from .utils import geocodificar_endereco


@receiver(post_save, sender=PrestadorProfile)
def atualizar_coordenadas(sender, instance, **kwargs):
    """
    Após salvar um PrestadorProfile, busca as coordenadas
    automaticamente se ainda não tiver ou se o endereço mudou.
    """
    if not instance.latitude or not instance.longitude:
        lat, lng = geocodificar_endereco(
            endereco=instance.usuario.address or '',
            cidade=instance.cidade
        )
        if lat and lng:
            # Atualiza sem disparar o signal novamente (evita loop infinito)
            PrestadorProfile.objects.filter(pk=instance.pk).update(
                latitude=lat,
                longitude=lng
            )

