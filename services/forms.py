from django import forms
from .models import Service, Pedido


class ServiceForm(forms.ModelForm):

    class Meta:
        model = Service
        fields = ['nome', 'descricao', 'categoria', 'preco']


class PedidoForm(forms.ModelForm):

    class Meta:
        model = Pedido
        fields = []