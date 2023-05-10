from django.shortcuts import render
from .models import Evento, EventDates
from django.contrib.auth.decorators import login_required


# Create your views here.
def evento(request):
    curr_user = request.user

    return render(request, 'conteudos_bi.html')


