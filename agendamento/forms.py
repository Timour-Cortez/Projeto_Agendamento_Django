from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Agendamento, ConfiguracaoSite, Servico


class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['cliente', 'servico', 'local', 'data', 'horario', 'observacoes']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'horario': forms.TimeInput(attrs={'type': 'time'}),
            'observacoes': forms.Textarea(attrs={'rows': 4}),
        }


class ConfiguracaoSiteForm(forms.ModelForm):
    class Meta:
        model = ConfiguracaoSite
        fields = ['nome_site', 'titulo_home', 'texto_home', 'logo', 'paleta_cores']
        labels = {
            'nome_site': 'Nome da empresa',
            'titulo_home': 'Título principal da tela inicial',
            'texto_home': 'Texto da tela inicial',
            'logo': 'Logo do site',
            'paleta_cores': 'Paleta de cores',
        }
        widgets = {
            'nome_site': forms.TextInput(attrs={
                'placeholder': 'Ex: Atobá Drones'
            }),
            'titulo_home': forms.TextInput(attrs={
                'placeholder': 'Ex: Filmagens aéreas profissionais com drones'
            }),
            'texto_home': forms.TextInput(attrs={
                'placeholder': 'Ex: Agende seu serviço com segurança, qualidade e planejamento.'
            }),
        }


class ServicoDashboardForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['nome', 'descricao', 'preco', 'duracao_estimada', 'ativo']
        labels = {
            'nome': 'Nome do pacote',
            'descricao': 'Descrição',
            'preco': 'Preço',
            'duracao_estimada': 'Duração estimada em minutos',
            'ativo': 'Exibir este pacote na tela inicial',
        }
        widgets = {
            'descricao': forms.Textarea(attrs={
                'rows': 4
            }),
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


NOTA_CHOICES = [
    ('1', '1 estrela'),
    ('2', '2 estrelas'),
    ('3', '3 estrelas'),
    ('4', '4 estrelas'),
    ('5', '5 estrelas'),
]


class ReclamacaoForm(forms.Form):
    nome = forms.CharField(label='Nome', max_length=100)
    email = forms.EmailField(label='E-mail')
    servico_contratado = forms.CharField(label='Serviço contratado', max_length=200)
    descricao = forms.CharField(label='Descrição da reclamação', widget=forms.Textarea)
    nota = forms.ChoiceField(label='Avaliação', choices=NOTA_CHOICES)


class EditarAgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['data', 'horario', 'observacoes']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'horario': forms.TimeInput(attrs={'type': 'time'}),
            'observacoes': forms.Textarea(attrs={'rows': 4}),
        }
