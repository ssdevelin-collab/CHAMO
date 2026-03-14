# avaliacoes/forms.py

from django import forms
from .models import AvaliacaoCliente, AvaliacaoPrestador


class AvaliacaoClienteForm(forms.ModelForm):
    class Meta:
        model = AvaliacaoCliente
        fields = ['nota', 'comentario']
        widgets = {
            'nota': forms.HiddenInput(),
            'comentario': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Conte como foi sua experiência... (opcional)',
                'class': 'form-control'
            }),
        }


class AvaliacaoPrestadorForm(forms.ModelForm):
    class Meta:
        model = AvaliacaoPrestador
        fields = ['nota', 'comentario']
        widgets = {
            'nota': forms.HiddenInput(),
            'comentario': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Conte como foi sua experiência com o cliente... (opcional)',
                'class': 'form-control'
            }),
        }