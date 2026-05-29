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


class CadastroForm(forms.Form):
    nome = forms.CharField(label='Nome completo', max_length=150)
    email = forms.EmailField(label='E-mail')
    senha = forms.CharField(label='Senha', widget=forms.PasswordInput)
    confirmar_senha = forms.CharField(label='Confirmar senha', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get('senha')
        confirmar_senha = cleaned_data.get('confirmar_senha')
        if senha and confirmar_senha and senha != confirmar_senha:
            raise forms.ValidationError('As senhas não coincidem.')
        return cleaned_data


class EsqueciSenhaForm(forms.Form):
    email = forms.EmailField(label='E-mail')