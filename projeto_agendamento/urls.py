"""
URL configuration for projeto_agendamento project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('agendamento.urls')),

    path('esqueci-senha/', auth_views.PasswordResetView.as_view(
        template_name='esqueci_senha.html',
        email_template_name='email_redefinir_senha.html',
        success_url='/esqueci-senha/enviado/'
    ), name='esqueci_senha'),

    path('esqueci-senha/enviado/', auth_views.PasswordResetDoneView.as_view(
        template_name='esqueci_senha_sucesso.html'
    ), name='password_reset_done'),

    path('redefinir-senha/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='redefinir_senha.html',
        success_url='/redefinir-senha/concluido/'
    ), name='password_reset_confirm'),

    path('redefinir-senha/concluido/', auth_views.PasswordResetCompleteView.as_view(
        template_name='redefinir_senha_sucesso.html'
    ), name='password_reset_complete'),
]
