from django.shortcuts import render
from .models import Event, EventDates
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth.models import User


# Create your views here.
@login_required
def cadastro_eventos(request):
    curr_user = request.user

    if request.method == "POST":
        response = request.POST

        print(response)

        try:
            if (response['meia']):
                meia = True
        except:
            meia = False
        
        try:
            if (response['comunitario']):
                comunitario = True
        except:
            comunitario = False

        try:
            if (response['gratuito']):
                gratuito = True
        except:
            gratuito = False
        
        try:
            preco = response['preco']
            if preco == '':
                preco = 0
        except:
            preco = 0

        

        event = Event(
            nome=response['nome'],
            descricao=response['descricao'],
            preco_ingresso=preco,
            ingresso_meia=meia,
            ingresso_comunitario=comunitario,
            gratuito=gratuito,
            usuario=curr_user
        )

        event.save()

        number_of_dates = int(response['number_of_dates'])
        if int(number_of_dates) > 0:
            for i in range(0, number_of_dates):
                if response['data_{}'.format(i)]:
                    date_obj = datetime.strptime(response['data_{}'.format(i)], '%Y-%m-%d')

                    time_obj = datetime.strptime(response['hora_{}'.format(i)], '%H:%M').time()

                    date_event = EventDates(
                        evento=event,
                        date=datetime.combine(date_obj, time_obj),
                        uso=response['tipo_{}'.format(i)]
                    )

                    date_event.save()
        else:
            date_obj = datetime.strptime(response['data_0'], '%Y-%m-%d')

            time_obj = datetime.strptime(response['hora_0'], '%H:%M').time()

            date_event = EventDates(
                evento=event,
                date=datetime.combine(date_obj, time_obj),
                uso=response['tipo_0']
            )

            date_event.save()

    return render(request, 'cadastroEvento.html')


def eventos(request):
    return render(request, 'index.html')
