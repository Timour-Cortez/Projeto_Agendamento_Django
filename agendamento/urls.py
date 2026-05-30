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
    path('prestador/dashboard/', views.prestador_dashboard, name='prestador_dashboard'),
    path('cliente/pedido/<int:pedido_id>/acompanhar/', views.cliente_acompanhamento, name='cliente_acompanhamento'),
    path('reclame-aqui/', views.reclame_aqui, name='reclame_aqui'),
]