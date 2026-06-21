from django.contrib import admin
from .models import Servico, Cliente, LocalAtendimento, Agendamento, DiaBloqueado, HorarioDisponivel


admin.site.register(Cliente)
admin.site.register(Servico)
admin.site.register(LocalAtendimento)
admin.site.register(Agendamento)
admin.site.register(DiaBloqueado)
admin.site.register(HorarioDisponivel)
