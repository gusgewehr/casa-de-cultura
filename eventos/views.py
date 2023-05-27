from django.shortcuts import render
from .models import Event, EventDates
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth.models import User


# Create your views here.
def cadastro_eventos(request):
    curr_user = request.user

    if request.method == "POST":
        response = request.POST

        print(response)

        if (response['meia']):
            meia = True
        else:
            meia = False

        if (response['comunitario']):
            comunitario = True
        else:
            comunitario = False

        event = Event(
            nome=response['nome'],
            descricao=response['descricao'],
            preco_ingresso=response['preco'],
            ingresso_meia=meia,
            ingresso_comunitario=comunitario,
            usuario=User.objects.get(pk=1)
        )

        event.save()

        date_obj = datetime.strptime(response['data'], '%Y-%m-%d')

        time_obj = datetime.strptime(response['hora'], '%H:%M').time()

        date_event = EventDates(
            evento=event,
            date=datetime.combine(date_obj, time_obj),
            uso=response['tipo']
        )

        date_event.save()

    return render(request, 'cadastroEvento.html')


def eventos(request):
    return render(request, 'index.html')
