from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .models import Servico
from .forms import AgendamentoForm, CadastroUsuarioForm, LoginUsuarioForm


def home(request):
    servicos = Servico.objects.all()
    return render(request, 'index.html', {'servicos': servicos})


def login_view(request):
    if request.method == 'POST':
        form = LoginUsuarioForm(request, data=request.POST)

        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)

            if 'pedido' in request.session:
                return redirect('pagamento')

            return redirect('home')
    else:
        form = LoginUsuarioForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


def cadastro(request):
    if request.method == 'POST':
        form = CadastroUsuarioForm(request.POST)

        if form.is_valid():
            usuario = form.save()
            login(request, usuario)

            if 'pedido' in request.session:
                return redirect('pagamento')

            return redirect('home')
    else:
        form = CadastroUsuarioForm()

    return render(request, 'cadastro.html', {'form': form})


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
            return redirect('pagamento')
        else:
            return redirect('login')

    return redirect('home')

def pagamento(request):
    pedido = request.session.get('pedido')

    if not request.user.is_authenticated:
        return redirect('login')

    if not pedido:
        return redirect('home')

    return render(request, 'pagamento.html', {'pedido': pedido})



def prestador_dashboard(request):
    from django.shortcuts import render
    return render(request, 'agendamento/prestador_dashboard.html', {
        'prestador': {'nome': 'Prestador'},
        'pedidos': [],
        'total_pedidos': 0,
        'pedidos_pendentes': 0,
        'pedidos_confirmados': 0,
    })

def cliente_acompanhamento(request, pedido_id):
    from django.shortcuts import render
    return render(request, 'agendamento/cliente_acompanhamento.html', {
        'pedido': None,
    })

