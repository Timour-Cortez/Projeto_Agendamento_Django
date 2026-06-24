from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

from django.utils import timezone

from .models import (
    Servico,
    Cliente,
    LocalAtendimento,
    Agendamento,
    PedidoPendente,
    DiaBloqueado,
    HorarioDisponivel,
    ConfiguracaoSite,
)

from .forms import (
    AgendamentoForm,
    CadastroUsuarioForm,
    LoginUsuarioForm,
    ReclamacaoForm,
    EditarAgendamentoForm,
    ConfiguracaoSiteForm,
    ServicoDashboardForm,
)


def reserva_ainda_valida():
    return timezone.now() - timedelta(minutes=15)


def home(request):
    servicos = Servico.objects.filter(
        ativo=True
    ).order_by('nome')

    horarios_disponiveis = HorarioDisponivel.objects.filter(
        ativo=True
    ).order_by('horario')

    dias_bloqueados = DiaBloqueado.objects.values_list('data', flat=True)

    datas_indisponiveis = []

    for data in dias_bloqueados:
        datas_indisponiveis.append(data.strftime('%Y-%m-%d'))

    agendamentos_confirmados = Agendamento.objects.filter(
        status='confirmado'
    ).order_by('data', 'horario')

    pedidos_pendentes_validos = PedidoPendente.objects.filter(
        status_pagamento='aguardando_pagamento',
        criado_em__gte=reserva_ainda_valida()
    ).order_by('data', 'horario')

    horarios_ocupados_por_data = {}

    for agendamento in agendamentos_confirmados:
        data_formatada = agendamento.data.strftime('%Y-%m-%d')
        horario_formatado = agendamento.horario.strftime('%H:%M')

        if data_formatada not in horarios_ocupados_por_data:
            horarios_ocupados_por_data[data_formatada] = []

        horarios_ocupados_por_data[data_formatada].append(horario_formatado)

    for pedido_pendente in pedidos_pendentes_validos:
        data_formatada = pedido_pendente.data.strftime('%Y-%m-%d')
        horario_formatado = pedido_pendente.horario.strftime('%H:%M')

        if data_formatada not in horarios_ocupados_por_data:
            horarios_ocupados_por_data[data_formatada] = []

        if horario_formatado not in horarios_ocupados_por_data[data_formatada]:
            horarios_ocupados_por_data[data_formatada].append(horario_formatado)

    return render(request, 'index.html', {
        'servicos': servicos,
        'horarios_disponiveis': horarios_disponiveis,
        'datas_indisponiveis': datas_indisponiveis,
        'horarios_ocupados_por_data': horarios_ocupados_por_data,
    })


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
        horario_servico = request.POST.get('horario_servico')

        servico = Servico.objects.get(id=servico_id)

        request.session.pop('pedido_pendente_id', None)

        request.session['pedido'] = {
            'servico_id': servico_id,
            'servico_nome': servico.nome,
            'servico_preco': str(servico.preco),
            'endereco': endereco,
            'latitude': latitude,
            'longitude': longitude,
            'data_servico': data_servico,
            'horario_servico': horario_servico,
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

    pedido_pendente_id = request.session.get('pedido_pendente_id')
    pedido_pendente = None

    if pedido_pendente_id:
        pedido_pendente = PedidoPendente.objects.filter(
            id=pedido_pendente_id,
            usuario=request.user,
            status_pagamento='aguardando_pagamento'
        ).first()

    if not pedido_pendente:
        servico = Servico.objects.get(id=pedido['servico_id'])
        horario_escolhido = datetime.strptime(pedido['horario_servico'], '%H:%M').time()

        dia_bloqueado = DiaBloqueado.objects.filter(
            data=pedido['data_servico']
        ).exists()

        if dia_bloqueado:
            del request.session['pedido']
            messages.error(
                request,
                'Essa data foi bloqueada pelo prestador. Escolha outra data para continuar.'
            )
            return redirect('home')

        horario_ocupado = Agendamento.objects.filter(
            data=pedido['data_servico'],
            horario=horario_escolhido,
            status='confirmado'
        ).exists()

        if horario_ocupado:
            del request.session['pedido']
            messages.error(
                request,
                'Esse horário acabou de ficar indisponível. Escolha outro horário para continuar.'
            )
            return redirect('home')

        pedido_pendente_ocupando = PedidoPendente.objects.filter(
            data=pedido['data_servico'],
            horario=horario_escolhido,
            status_pagamento='aguardando_pagamento',
            criado_em__gte=reserva_ainda_valida()
        ).exists()

        if pedido_pendente_ocupando:
            del request.session['pedido']
            messages.error(
                request,
                'Esse horário acabou de ficar temporariamente reservado. Escolha outro horário para continuar.'
            )
            return redirect('home')

        horario_ativo = HorarioDisponivel.objects.filter(
            horario=horario_escolhido,
            ativo=True
        ).exists()

        if not horario_ativo:
            del request.session['pedido']
            messages.error(
                request,
                'Esse horário não está mais disponível. Escolha outro horário para continuar.'
            )
            return redirect('home')

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

        pedido_pendente = PedidoPendente.objects.create(
            usuario=request.user,
            cliente=cliente,
            servico=servico,
            local=local,
            data=pedido['data_servico'],
            horario=horario_escolhido,
            valor=servico.preco,
            status_pagamento='aguardando_pagamento'
        )

        request.session['pedido_pendente_id'] = pedido_pendente.id

    return render(request, 'pagamento.html', {
        'pedido': pedido,
        'pedido_pendente': pedido_pendente,
    })


@login_required
def confirmar_pedido(request):
    if request.method != 'POST':
        return redirect('pagamento')

    pedido = request.session.get('pedido')
    pedido_pendente_id = request.session.get('pedido_pendente_id')

    if not pedido or not pedido_pendente_id:
        return redirect('home')

    pedido_pendente = PedidoPendente.objects.filter(
        id=pedido_pendente_id,
        usuario=request.user,
        status_pagamento='aguardando_pagamento'
    ).first()

    if not pedido_pendente:
        messages.error(
            request,
            'Não foi possível encontrar um pagamento pendente para este pedido.'
        )
        return redirect('home')

    if pedido_pendente.criado_em < reserva_ainda_valida():
        pedido_pendente.status_pagamento = 'expirado'
        pedido_pendente.save()

        request.session.pop('pedido', None)
        request.session.pop('pedido_pendente_id', None)

        messages.error(
            request,
            'O tempo de reserva desse horário expirou. Escolha outro horário para continuar.'
        )
        return redirect('home')

    dia_bloqueado = DiaBloqueado.objects.filter(
        data=pedido_pendente.data
    ).exists()

    if dia_bloqueado:
        pedido_pendente.status_pagamento = 'recusado'
        pedido_pendente.save()

        request.session.pop('pedido', None)
        request.session.pop('pedido_pendente_id', None)

        messages.error(
            request,
            'Essa data foi bloqueada pelo prestador. Escolha outra data para continuar.'
        )
        return redirect('home')

    horario_ocupado = Agendamento.objects.filter(
        data=pedido_pendente.data,
        horario=pedido_pendente.horario,
        status='confirmado'
    ).exists()

    if horario_ocupado:
        pedido_pendente.status_pagamento = 'recusado'
        pedido_pendente.save()

        request.session.pop('pedido', None)
        request.session.pop('pedido_pendente_id', None)

        messages.error(
            request,
            'Esse horário acabou de ficar indisponível. Escolha outro horário para continuar.'
        )
        return redirect('home')

    pedido_pendente.status_pagamento = 'aprovado'
    pedido_pendente.pagamento_id = f'SIMULADO-{pedido_pendente.id}'
    pedido_pendente.save()

    Agendamento.objects.create(
        usuario=request.user,
        cliente=pedido_pendente.cliente,
        servico=pedido_pendente.servico,
        local=pedido_pendente.local,
        data=pedido_pendente.data,
        horario=pedido_pendente.horario,
        status='confirmado',
        observacoes='Pedido criado após pagamento simulado aprovado.'
    )

    request.session.pop('pedido', None)
    request.session.pop('pedido_pendente_id', None)

    messages.success(
        request,
        'Pagamento aprovado. Pedido confirmado com sucesso.'
    )

    return redirect('meus_agendamentos')


@login_required
def pagamento_recusado(request):
    if request.method != 'POST':
        return redirect('pagamento')

    pedido_pendente_id = request.session.get('pedido_pendente_id')

    if pedido_pendente_id:
        pedido_pendente = PedidoPendente.objects.filter(
            id=pedido_pendente_id,
            usuario=request.user,
            status_pagamento='aguardando_pagamento'
        ).first()

        if pedido_pendente:
            pedido_pendente.status_pagamento = 'recusado'
            pedido_pendente.pagamento_id = f'SIMULADO-RECUSADO-{pedido_pendente.id}'
            pedido_pendente.save()

    request.session.pop('pedido', None)
    request.session.pop('pedido_pendente_id', None)

    messages.error(
        request,
        'Pagamento recusado. O pedido não foi lançado no sistema.'
    )

    return redirect('home')


@login_required
def meus_agendamentos(request):
    agendamentos_confirmados = Agendamento.objects.filter(
        usuario=request.user,
        status='confirmado'
    ).order_by('data', 'horario')

    agendamentos_historico = Agendamento.objects.filter(
        usuario=request.user,
        status__in=['concluido', 'cancelado']
    ).order_by('-data', '-horario')

    return render(request, 'meus_agendamentos.html', {
        'agendamentos_confirmados': agendamentos_confirmados,
        'agendamentos_historico': agendamentos_historico,
    })


@login_required
def prestador_dashboard(request):
    if not request.user.is_staff:
        return redirect('home')

    configuracao, criado = ConfiguracaoSite.objects.get_or_create(
        id=1,
        defaults={
            'nome_site': 'Agenda Fácil',
            'texto_home': 'Agende serviços de forma simples, rápida e organizada.',
            'paleta_cores': 'verde_institucional',
        }
    )

    if request.method == 'POST':
        acao_pedido = request.POST.get('acao_pedido')
        agendamento_id = request.POST.get('agendamento_id')
        acao_horario = request.POST.get('acao_horario')
        acao_configuracao = request.POST.get('acao_configuracao')
        acao_servico = request.POST.get('acao_servico')

        if acao_configuracao == 'salvar':
            configuracao_form = ConfiguracaoSiteForm(
                request.POST,
                request.FILES,
                instance=configuracao
            )

            if configuracao_form.is_valid():
                configuracao_form.save()
                messages.success(request, 'Personalização do site salva com sucesso.')
            else:
                messages.error(request, 'Não foi possível salvar a personalização.')

            return redirect('prestador_dashboard')

        if acao_servico:
            servico_id = request.POST.get('servico_id')

            if acao_servico == 'criar':
                servico_form = ServicoDashboardForm(request.POST)

                if servico_form.is_valid():
                    servico_form.save()
                    messages.success(request, 'Pacote criado com sucesso.')
                else:
                    messages.error(request, 'Não foi possível criar o pacote.')

            elif acao_servico == 'editar':
                servico = Servico.objects.filter(id=servico_id).first()

                if servico:
                    servico_form = ServicoDashboardForm(request.POST, instance=servico)

                    if servico_form.is_valid():
                        servico_form.save()
                        messages.success(request, 'Pacote atualizado com sucesso.')
                    else:
                        messages.error(request, 'Não foi possível atualizar o pacote.')

            elif acao_servico in ['ativar', 'desativar']:
                servico = Servico.objects.filter(id=servico_id).first()

                if servico:
                    if acao_servico == 'ativar':
                        servico.ativo = True
                        messages.success(request, 'Pacote ativado com sucesso.')

                    elif acao_servico == 'desativar':
                        servico.ativo = False
                        messages.success(request, 'Pacote desativado com sucesso.')

                    servico.save()

            return redirect('prestador_dashboard')

        if acao_pedido and agendamento_id:
            agendamento = Agendamento.objects.filter(id=agendamento_id).first()

            if agendamento:
                if acao_pedido == 'confirmar':
                    agendamento.status = 'confirmado'

                elif acao_pedido == 'concluir':
                    agendamento.status = 'concluido'

                elif acao_pedido == 'cancelar':
                    agendamento.status = 'cancelado'

                agendamento.save()

            return redirect('prestador_dashboard')

        if acao_horario:
            if acao_horario == 'adicionar':
                novo_horario = request.POST.get('novo_horario')

                if novo_horario:
                    horario_convertido = datetime.strptime(novo_horario, '%H:%M').time()

                    horario_obj, criado = HorarioDisponivel.objects.get_or_create(
                        horario=horario_convertido,
                        defaults={
                            'ativo': True
                        }
                    )

                    if not criado:
                        horario_obj.ativo = True
                        horario_obj.save()

            elif acao_horario in ['ativar', 'desativar']:
                horario_id = request.POST.get('horario_id')
                horario_obj = HorarioDisponivel.objects.filter(id=horario_id).first()

                if horario_obj:
                    if acao_horario == 'ativar':
                        horario_obj.ativo = True

                    elif acao_horario == 'desativar':
                        horario_obj.ativo = False

                    horario_obj.save()

            return redirect('prestador_dashboard')

        data_bloqueio = request.POST.get('data_bloqueio')
        motivo_bloqueio = request.POST.get('motivo_bloqueio')

        if data_bloqueio:
            DiaBloqueado.objects.get_or_create(
                data=data_bloqueio,
                defaults={
                    'motivo': motivo_bloqueio
                }
            )

        return redirect('prestador_dashboard')

    pedidos = Agendamento.objects.all().order_by('data', 'horario')

    agendamentos_a_fazer = Agendamento.objects.filter(
        status='confirmado'
    ).order_by('data', 'horario')

    agendamentos_historico = Agendamento.objects.filter(
        status__in=['concluido', 'cancelado']
    ).order_by('-data', '-horario')

    dias_bloqueados = DiaBloqueado.objects.all().order_by('data')

    datas_bloqueadas = []

    for dia in dias_bloqueados:
        datas_bloqueadas.append(dia.data.strftime('%Y-%m-%d'))

    datas_com_servico = []

    for agendamento in agendamentos_a_fazer:
        datas_com_servico.append(agendamento.data.strftime('%Y-%m-%d'))

    eventos_calendario = []

    for agendamento in agendamentos_a_fazer:
        eventos_calendario.append({
            'id': agendamento.id,
            'data': agendamento.data.strftime('%Y-%m-%d'),
            'servico': agendamento.servico.nome,
            'cliente': agendamento.cliente.nome,
            'email': agendamento.cliente.email,
            'endereco': agendamento.local.endereco,
            'horario': agendamento.horario.strftime('%H:%M'),
            'status': agendamento.status,
            'observacoes': agendamento.observacoes or '',
        })

    horarios_dashboard = HorarioDisponivel.objects.all().order_by('horario')
    servicos_dashboard = Servico.objects.all().order_by('nome')

    total_a_fazer = agendamentos_a_fazer.count()
    total_historico = agendamentos_historico.count()
    total_pendentes = Agendamento.objects.filter(status='pendente').count()
    total_confirmados = Agendamento.objects.filter(status='confirmado').count()

    return render(request, 'staff_dashboard.html', {
        'pedidos': pedidos,
        'agendamentos_a_fazer': agendamentos_a_fazer,
        'agendamentos_historico': agendamentos_historico,
        'dias_bloqueados': dias_bloqueados,
        'datas_bloqueadas': datas_bloqueadas,
        'datas_com_servico': datas_com_servico,
        'eventos_calendario': eventos_calendario,
        'horarios_dashboard': horarios_dashboard,
        'servicos_dashboard': servicos_dashboard,
        'total_a_fazer': total_a_fazer,
        'total_historico': total_historico,
        'total_pendentes': total_pendentes,
        'total_confirmados': total_confirmados,
    })


def cliente_acompanhamento(request, pedido_id=None):
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
