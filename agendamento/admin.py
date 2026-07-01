from django.contrib import admin
from .models import Cliente, Servico, LocalAtendimento, Agendamento, PlanoAssinatura, Assinatura, Prestador

admin.site.register(PlanoAssinatura)
admin.site.register(Assinatura)

admin.site.register(Cliente)
admin.site.register(Servico)
admin.site.register(LocalAtendimento)
admin.site.register(Agendamento)
