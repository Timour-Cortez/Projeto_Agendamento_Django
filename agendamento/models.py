from django.db import models
from django.contrib.auth.models import User


class ConfiguracaoSite(models.Model):
    PALETA_CHOICES = [
        ('verde_institucional', 'Verde institucional'),
        ('azul_profissional', 'Azul profissional'),
        ('areia_minimalista', 'Areia minimalista'),

        ('preto_premium', 'Preto premium'),
        ('grafite_tecnologico', 'Grafite tecnológico'),
        ('azul_marinho_executivo', 'Azul marinho executivo'),
        ('vermelho_energia', 'Vermelho energia'),
        ('laranja_criativo', 'Laranja criativo'),
        ('roxo_moderno', 'Roxo moderno'),
        ('rosa_elegante', 'Rosa elegante'),
        ('verde_saude', 'Verde saúde'),
        ('azul_claro_leve', 'Azul claro leve'),
        ('marrom_artesanal', 'Marrom artesanal'),
    ]

    nome_site = models.CharField(
        max_length=100,
        default='Atobá Drones'
    )
    titulo_home = models.CharField(
        max_length=120,
        default='Filmagens aéreas profissionais com drones'
    )
    texto_home = models.CharField(
        max_length=200,
        default='Agende seu serviço com segurança, qualidade e planejamento.'
    )
    logo = models.FileField(upload_to='logos/', blank=True, null=True)
    paleta_cores = models.CharField(
        max_length=30,
        choices=PALETA_CHOICES,
        default='verde_institucional'
    )

    def __str__(self):
        return self.nome_site

    @property
    def cor_principal(self):
        cores = {
            'verde_institucional': '#6b7b4b',
            'azul_profissional': '#2f5f7f',
            'areia_minimalista': '#9c7b4f',

            'preto_premium': '#1f1f1f',
            'grafite_tecnologico': '#2b2f36',
            'azul_marinho_executivo': '#1f3a5f',
            'vermelho_energia': '#9b2f2f',
            'laranja_criativo': '#c76b2c',
            'roxo_moderno': '#5b3f8c',
            'rosa_elegante': '#b05a7a',
            'verde_saude': '#3f7f5f',
            'azul_claro_leve': '#3f88a8',
            'marrom_artesanal': '#7a4f35',
        }
        return cores.get(self.paleta_cores, '#6b7b4b')

    @property
    def cor_secundaria(self):
        cores = {
            'verde_institucional': '#eef3e4',
            'azul_profissional': '#e4eef3',
            'areia_minimalista': '#f3ede4',

            'preto_premium': '#f2f2f2',
            'grafite_tecnologico': '#e8eaed',
            'azul_marinho_executivo': '#e6edf5',
            'vermelho_energia': '#f5e3e3',
            'laranja_criativo': '#f7eadf',
            'roxo_moderno': '#eee7f7',
            'rosa_elegante': '#f7e6ee',
            'verde_saude': '#e5f3eb',
            'azul_claro_leve': '#e4f3f8',
            'marrom_artesanal': '#f1e7df',
        }
        return cores.get(self.paleta_cores, '#eef3e4')


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
    duracao_estimada = models.PositiveIntegerField(help_text='Duração em minutos')
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class LocalAtendimento(models.Model):
    endereco = models.CharField(max_length=200)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    referencia = models.TextField(blank=True)

    def __str__(self):
        return f'{self.endereco} - {self.bairro}'


class Agendamento(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('concluido', 'Concluído'),
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
        return f'{self.cliente.nome} - {self.servico.nome} - {self.data} {self.horario}'


class DiaBloqueado(models.Model):
    data = models.DateField(unique=True)
    motivo = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f'{self.data} - {self.motivo}'


class HorarioDisponivel(models.Model):
    horario = models.TimeField(unique=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.horario.strftime('%H:%M')
