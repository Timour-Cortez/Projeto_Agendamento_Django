from django.db import models
from django.contrib.auth.models import User


class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return self.nome


class Servico(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    duracao_estimada = models.PositiveIntegerField(help_text="Duração em minutos")

    def __str__(self):
        return self.nome


class LocalAtendimento(models.Model):
    endereco = models.CharField(max_length=200)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    referencia = models.TextField(blank=True)

    def __str__(self):
        return f"{self.endereco} - {self.bairro}"


class Agendamento(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    local = models.ForeignKey(LocalAtendimento, on_delete=models.CASCADE)
    data = models.DateField()
    horario = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    observacoes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.cliente.nome} - {self.servico.nome} - {self.data} {self.horario}"


class DiaBloqueado(models.Model):
    data = models.DateField(unique=True)
    motivo = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.data} - {self.motivo}"