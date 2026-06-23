from .models import ConfiguracaoSite


def configuracao_site(request):
    configuracao, criado = ConfiguracaoSite.objects.get_or_create(
        id=1,
        defaults={
            'nome_site': 'Atobá Drones',
            'titulo_home': 'Filmagens aéreas profissionais com drones',
            'texto_home': 'Agende seu serviço com segurança, qualidade e planejamento.',
            'paleta_cores': 'verde_institucional',
        }
    )

    return {
        'configuracao_site': configuracao
    }
