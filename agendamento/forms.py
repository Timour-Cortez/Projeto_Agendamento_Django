from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Agendamento


class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['cliente', 'servico', 'local', 'data', 'horario', 'observacoes']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'horario': forms.TimeInput(attrs={'type': 'time'}),
            'observacoes': forms.Textarea(attrs={'rows': 4}),
        }


class CadastroUsuarioForm(UserCreationForm):
    username = forms.CharField(
        label='Nome de usuário',
        help_text=''
    )

    email = forms.EmailField(
        label='E-mail',
        required=True
    )

    password1 = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput,
        help_text=''
    )

    password2 = forms.CharField(
        label='Confirme sua senha',
        widget=forms.PasswordInput,
        help_text=''
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginUsuarioForm(AuthenticationForm):
    username = forms.CharField(
        label='Nome de usuário'
    )

    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput
    )