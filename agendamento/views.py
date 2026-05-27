from django.shortcuts import render, redirect
from .models import Servico
from .forms import AgendamentoForm


def home(request):
    servicos = Servico.objects.all()
    return render(request, 'index.html', {'servicos': servicos})


def login(request):
    return render(request, 'login.html')


def agendar(request):
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AgendamentoForm()

    return render(request, 'agendar.html', {'form': form})