from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, PrestadorProfile


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'username',
            'full_name',
            'email',
            'cpf',
            'phone',
            'birth_date',
            'address',
            'city',
            'user_type',
            'password1',
            'password2',
        ]


class PrestadorProfileForm(forms.ModelForm):

    class Meta:
        model = PrestadorProfile
        fields = [
            'nome_empresa',
            'descricao',
            'cidade',
            'categoria',
            'foto',
        ]