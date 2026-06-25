from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('agendar/', views.agendar, name='agendar'),
    path('montar-pedido/', views.montar_pedido, name='montar_pedido'),
    path('pagamento/', views.pagamento, name='pagamento'),

    path('confirmar-pedido/', views.confirmar_pedido, name='confirmar_pedido'),
    path('pagamento/recusado/', views.pagamento_recusado, name='pagamento_recusado'),
    path('pagamento/asaas/', views.iniciar_pagamento_asaas, name='iniciar_pagamento_asaas'),

    path('pagamento/retorno/sucesso/', views.retorno_pagamento_sucesso, name='retorno_pagamento_sucesso'),
    path('pagamento/retorno/falha/', views.retorno_pagamento_falha, name='retorno_pagamento_falha'),
    path('webhook/asaas/', views.webhook_asaas, name='webhook_asaas'),

    path('meus-agendamentos/', views.meus_agendamentos, name='meus_agendamentos'),

    path('agendamento/<int:agendamento_id>/editar/', views.editar_agendamento, name='editar_agendamento'),
    path('agendamento/<int:agendamento_id>/cancelar/', views.cancelar_agendamento, name='cancelar_agendamento'),

    path('prestador/dashboard/', views.prestador_dashboard, name='prestador_dashboard'),
    path('cliente/pedido/<int:pedido_id>/acompanhar/', views.cliente_acompanhamento, name='cliente_acompanhamento'),
    path('reclame-aqui/', views.reclame_aqui, name='reclame_aqui'),
    path('acompanhamento/', views.cliente_acompanhamento, name='cliente_acompanhamento'),
]
