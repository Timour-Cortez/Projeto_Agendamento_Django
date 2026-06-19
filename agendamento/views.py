from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from datetime import time

from .models import Servico, Cliente, LocalAtendimento, Agendamento
from .forms import AgendamentoForm, CadastroUsuarioForm, LoginUsuarioForm, ReclamacaoForm, EditarAgendamentoForm


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


@login_required
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


@login_required
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
            'servico_nome': Servico.objects.get(id=servico_id).nome,
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


@login_required
def pagamento(request):
    pedido = request.session.get('pedido')

    if not pedido:
        return redirect('home')

    return render(request, 'pagamento.html', {'pedido': pedido})


@login_required
def confirmar_pedido(request):
    pedido = request.session.get('pedido')

    if not pedido:
        return redirect('home')

    servico = Servico.objects.get(id=pedido['servico_id'])

    cliente, criado = Cliente.objects.get_or_create(
        email=request.user.email,
        defaults={
            'nome': request.user.username,
            'telefone': ''
        }
    )

    local = LocalAtendimento.objects.create(
        endereco=pedido['endereco'],
        bairro='Não informado',
        cidade='Rio de Janeiro',
        referencia=f"Latitude: {pedido['latitude']} | Longitude: {pedido['longitude']}"
    )

    Agendamento.objects.create(
        usuario=request.user,
        cliente=cliente,
        servico=servico,
        local=local,
        data=pedido['data_servico'],
        horario=time(9, 0),
        status='pendente',
        observacoes='Pedido criado pela página inicial.'
    )

    del request.session['pedido']

    return redirect('meus_agendamentos')


@login_required
def meus_agendamentos(request):
    agendamentos_pendentes = Agendamento.objects.filter(
        usuario=request.user,
        status='pendente'
    )

    agendamentos_confirmados = Agendamento.objects.filter(
        usuario=request.user,
        status='confirmado'
    )

    agendamentos_concluidos = Agendamento.objects.filter(
        usuario=request.user,
        status='concluido'
    )

    return render(request, 'meus_agendamentos.html', {
        'agendamentos_pendentes': agendamentos_pendentes,
        'agendamentos_confirmados': agendamentos_confirmados,
        'agendamentos_concluidos': agendamentos_concluidos,
    })


@login_required
def prestador_dashboard(request):
    pedidos = Agendamento.objects.all().order_by('data', 'horario')

    return render(request, 'agendamento/prestador_dashboard.html', {
        'pedidos': pedidos,
    })


@login_required
def cliente_acompanhamento(request, pedido_id):
    return render(request, 'agendamento/cliente_acompanhamento.html', {
        'pedido': None,
    })


def reclame_aqui(request):
    if request.method == 'POST':
        form = ReclamacaoForm(request.POST)

        if form.is_valid():
            return render(request, 'reclame_aqui_sucesso.html')
    else:
        form = ReclamacaoForm()

    return render(request, 'reclame_aqui.html', {'form': form})


@login_required
def editar_agendamento(request, agendamento_id):
    agendamento = Agendamento.objects.get(id=agendamento_id, usuario=request.user)

    if request.method == 'POST':
        form = EditarAgendamentoForm(request.POST, instance=agendamento)

        if form.is_valid():
            form.save()
            return redirect('meus_agendamentos')
    else:
        form = EditarAgendamentoForm(instance=agendamento)

    return render(request, 'editar_agendamento.html', {
        'form': form,
        'agendamento': agendamento
    })


@login_required
def cancelar_agendamento(request, agendamento_id):
    agendamento = Agendamento.objects.get(id=agendamento_id, usuario=request.user)

    if request.method == 'POST':
        agendamento.status = 'cancelado'
        agendamento.save()
        return redirect('meus_agendamentos')

    return render(request, 'cancelar_agendamento.html', {
        'agendamento': agendamento
    })
