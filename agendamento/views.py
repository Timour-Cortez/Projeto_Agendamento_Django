from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .models import Servico
from .forms import AgendamentoForm, CadastroUsuarioForm, LoginUsuarioForm, CadastroForm, EsqueciSenhaForm


def home(request):
    servicos = Servico.objects.all()
    return render(request, 'index.html', {'servicos': servicos})


def login_view(request):
    if request.method == 'POST':
        form = LoginUsuarioForm(request, data=request.POST)

        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            return redirect('home')
    else:
        form = LoginUsuarioForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


def cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)

        if form.is_valid():
            return render(request, 'cadastro_sucesso.html')
    else:
        form = CadastroForm()

    return render(request, 'cadastro.html', {'form': form})


def esqueci_senha(request):
    if request.method == 'POST':
        form = EsqueciSenhaForm(request.POST)

        if form.is_valid():
            return render(request, 'esqueci_senha_sucesso.html')
    else:
        form = EsqueciSenhaForm()

    return render(request, 'esqueci_senha.html', {'form': form})


def agendar(request):
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AgendamentoForm()

    return render(request, 'agendar.html', {'form': form})

def montar_pedido(request):
    if request.method == 'POST':
        servico_id = request.POST.get('servico_id')
        endereco = request.POST.get('endereco')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        data_servico = request.POST.get('data_servico')

        request.session['pedido'] = {
            'servico_id': servico_id,
            'endereco': endereco,
            'latitude': latitude,
            'longitude': longitude,
            'data_servico': data_servico,
        }

        if request.user.is_authenticated:
            return redirect('agendar')
        else:
            return redirect('login')

    return redirect('home')