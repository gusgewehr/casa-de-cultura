from django.shortcuts import render
from .models import Event, EventDates
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth.models import User
from django.core import serializers



# Create your views here.
@login_required
def cadastro_eventos(request):
    curr_user = request.user

    if request.method == "POST":
        response = request.POST


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

        
        try:
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
                    if response['date_{}'.format(i)]:
                        date_obj = datetime.strptime(response['date_{}'.format(i)], '%d/%M/%Y')

                        start_time_obj = datetime.strptime(response['start_time_{}'.format(i)], '%H:%M').time()
                        
                        end_time_obj = datetime.strptime(response['end_time_{}'.format(i)], '%H:%M').time()

                        date_event = EventDates(
                            evento=event,
                            start_date=datetime.combine(date_obj, start_time_obj),
                            end_date=datetime.combine(date_obj, end_time_obj),
                            uso=response['type_{}'.format(i)]
                        )

                        date_event.save()

                        print(date_event)
            else:
                date_obj = datetime.strptime(response['date_0'], '%d/%M/%Y')

                start_time_obj = datetime.strptime(response['start_time_0'], '%H:%M').time()
                        
                end_time_obj = datetime.strptime(response['end_time_0'], '%H:%M').time()

                date_event = EventDates(
                        evento=event,
                        start_date=datetime.combine(date_obj, start_time_obj),
                        end_date=datetime.combine(date_obj, end_time_obj),
                        uso=response['type_0']
                    )

                date_event.save()
            return render(request, 'cadastroEvento.html', {"post_status": True, 'status': True})
        except:
            return render(request, 'cadastroEvento.html', {"post_status": True, 'status': False})
    else:
        all_dates = EventDates.objects.all()
        return render(request, 'cadastroEvento.html', {'all_dates': serializers.serialize('json', all_dates)})

    


def eventos(request):
    return render(request, 'index.html')
