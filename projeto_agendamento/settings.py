import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-7_nl$-l_gv8+7cvuak#jtnf1daln6#y#50mtsib4(7^j!**rz3'

DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'fester-corned-unveiled.ngrok-free.dev',
    '.ngrok-free.dev',
    '.ngrok-free.app',
]

CSRF_TRUSTED_ORIGINS = [
    'https://fester-corned-unveiled.ngrok-free.dev',
]

INSTALLED_APPS = [
    'agendamento',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'projeto_agendamento.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'agendamento.context_processors.configuracao_site',
            ],
        },
    },
]


WSGI_APPLICATION = 'projeto_agendamento.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]


MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_URL = '/login/'


# Asaas Sandbox
# Configure no PowerShell antes de rodar o servidor:
# $env:ASAAS_API_KEY="SUA_CHAVE_API_SANDBOX"
ASAAS_API_KEY = os.environ.get('ASAAS_API_KEY', '')

ASAAS_BASE_URL = os.environ.get(
    'ASAAS_BASE_URL',
    'https://api-sandbox.asaas.com/v3'
)

# Usado só para teste enquanto o site ainda não coleta CPF/CNPJ do cliente.
# Em produção, o ideal é pedir CPF/CNPJ no cadastro ou na etapa de pagamento.
ASAAS_TEST_CPF_CNPJ = os.environ.get('ASAAS_TEST_CPF_CNPJ', '11144477735')

# Quando formos testar webhook real com ngrok, vamos colocar uma URL pública aqui.
# Exemplo:
# $env:ASAAS_PUBLIC_URL="https://seu-link-ngrok.ngrok-free.app"
ASAAS_PUBLIC_URL = os.environ.get('ASAAS_PUBLIC_URL', '')
