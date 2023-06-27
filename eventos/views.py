from django.shortcuts import render, get_object_or_404
from .models import Event, EventDates, EventImages
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth.models import User
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.conf import settings
from dateutil import relativedelta


# Create your views here.

def images_dir(instance, filename):
    date = timezone.now()
    month = date.month
    if month < 10:
        month = '0' + str(month)
    return f'{settings.MEDIA_ROOT}/imagens_eventos/{date.year}/{month}/{date.day}/{instance.nome}/{filename}'


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
                        date_obj = datetime.strptime(
                            response['date_{}'.format(i)], '%d/%m/%Y')
                        print(date_obj)

                        start_time_obj = datetime.strptime(
                            response['start_time_{}'.format(i)], '%H:%M').time()

                        end_time_obj = datetime.strptime(
                            response['end_time_{}'.format(i)], '%H:%M').time()

                        date_event = EventDates(
                            evento=event,
                            start_date=datetime.combine(
                                date_obj, start_time_obj),
                            end_date=datetime.combine(date_obj, end_time_obj),
                            uso=response['type_{}'.format(i)]
                        )

                        date_event.save()

            else:
                date_obj = datetime.strptime(response['date_0'], '%d/%m/%Y')
                print(date_obj)

                start_time_obj = datetime.strptime(
                    response['start_time_0'], '%H:%M').time()

                end_time_obj = datetime.strptime(
                    response['end_time_0'], '%H:%M').time()

                date_event = EventDates(
                    evento=event,
                    start_date=datetime.combine(date_obj, start_time_obj),
                    end_date=datetime.combine(date_obj, end_time_obj),
                    uso=response['type_0']
                )

                date_event.save()
            

            fss = FileSystemStorage()
            file = request.FILES['picture__input']
            event_image = EventImages(
                evento = event,
                image = fss.save(images_dir(event, file.name), file),
                is_cover = True
            )

            event_image.save()

            try:
                if (request.FILES['pictures_event_input']):
                    image_list = True
            except:
                image_list = False

                    
            if(image_list):
                fss2 = FileSystemStorage()    
                for f in request.FILES.getlist('pictures_event_input'):
                    event_image_from_list = EventImages(
                        evento = event,
                        image = fss2.save(images_dir(event, f.name), f),
                        is_cover = False
                    )
                    event_image_from_list.save()



            return render(request, 'cadastroEvento.html', {"post_status": True, 'status': True})
        except  Exception as err:
            event.delete()
            print('erro:  '+str(err))
            return render(request, 'cadastroEvento.html', {"post_status": True, 'status': False})
    else:
        all_dates = EventDates.objects.all()
        return render(request, 'cadastroEvento.html', {'all_dates': serializers.serialize('json', all_dates)})


def eventos(request):
    events = Event.objects.filter(aprovado = True) 
    event_dates = EventDates.objects.filter(
        uso = "AP", 
        evento__in = events,
        start_date__gte = datetime.now()
        
        ).distinct().order_by('start_date')
    images = EventImages.objects.filter(is_cover = True, evento__in = events).distinct()

    dict = []
    for date in event_dates:
        for event in events:
            if event == date.evento:
                evento = event
                break
            else:
                evento = None
        for img in images:
            if img.evento == date.evento:
                image = img
                break
            else:
                image = None

        dict.append( {
            'event': evento,
            'date': date,
            'image': image
        })

    context = {
        'dates': dict,
        'images': images,
        'range': range(len(dict))
        }

    #return render(request, 'index_old.html', context)
    return render(request, 'index.html', context)

@login_required
def meusEventos(request):

    events = Event.objects.filter(usuario = request.user) 
    event__future_dates = EventDates.objects.filter(
        evento__in = events,        
        ).distinct().order_by('start_date')
    #images = EventImages.objects.filter(is_cover = True, evento__in = events).distinct()

    dict_future_events = []
    dict_past_events = []
    for event in events:
        future_dates = []
        past_dates = []
        for date in event__future_dates:        
            if date.evento == event:
                if date.start_date > datetime.now():
                    future_dates.append(date)
                else:         
                    past_dates.append(date)

        if len(future_dates) >0 :
            dict_future_events.append( {
                'event': event,
                'dates': future_dates+past_dates,
            })
        else:
            dict_past_events.append({
                'event': event,
                'dates': past_dates,
            })


    event_date = EventDates.objects.all()

    event_list = Event.objects.all().filter(
        usuario=request.user)

    context = {
        'future_events': dict_future_events,
        'past_events': dict_past_events,
    }

    return render(request, 'myEvents.html', context)


def evento(request, id):
    event = get_object_or_404(Event, pk=id)
    date = EventDates.objects.order_by(
        '-start_date').filter(evento=event)
    images = EventImages.objects.filter(evento=event)

    context = {
        'event': event,
        'dates': date,
        'images': images
    }
    return render(request, 'evento.html', context)
