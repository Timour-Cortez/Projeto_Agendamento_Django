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
    path('meus-agendamentos/', views.meus_agendamentos, name='meus_agendamentos'),
]