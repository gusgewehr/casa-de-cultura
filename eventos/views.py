from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from .models import Event, EventDates, EventImages
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth.models import User
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.contrib import messages


# Create your views here.

def images_dir(instance, filename):
    date = timezone.now()
    month = date.month
    if month < 10:
        month = '0' + str(month)
    return f'{settings.MEDIA_ROOT}/imagens_eventos/{date.year}/{month}/{date.day}/{instance.nome}/{filename}'


@login_required
def cadastro_eventos(request, event_pk = None):

    curr_user = request.user

    all_dates = EventDates.objects.filter(
            start_date__gte=datetime.now()
        ).distinct().order_by('start_date')

    all_logged_dates = serializers.serialize('json', all_dates, indent = 2,use_natural_foreign_keys=True, use_natural_primary_keys=True)   

    if event_pk and request.method != 'POST':        
        
        evento = Event.objects.get(pk=event_pk)

        dates = EventDates.objects.filter(evento=evento)

        dates_json = serializers.serialize('json', dates)

        images = EventImages.objects.filter(evento=evento)

        event_images = []

        banner = ""

        for image in images:
            if image.is_cover:
                banner = image.image.url
            else:
                event_images.append(image.image.url)

        images_json = {
            "banner": banner,
            "event_images": event_images
        }

        if (curr_user == evento.usuario):
            return render(request, 'cadastroEvento.html', {
                'all_logged_dates': all_logged_dates, 
                'event':evento, 
                'event_dates': dates_json,
                'event_images': images_json

                })
        else:
            return render(request, PermissionDenied())

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
            id = response['event_id']
            old_event = Event.objects.get(id=id)
        except:
            id = None
        
        
################## atualizar evento ###############
        if id and curr_user == old_event.usuario:
            try:
                
                old_event.nome=response['nome']
                old_event.descricao=response['descricao']
                old_event.preco_ingresso=preco
                old_event.ingresso_meia=meia
                old_event.ingresso_comunitario=comunitario
                old_event.gratuito=gratuito

                old_event.save()

                old_dates = EventDates.objects.filter(evento=old_event)
                for date in old_dates:
                    date.delete()
                
                number_of_dates = int(response['number_of_dates'])
                if int(number_of_dates) > 0:
                    for i in range(0, number_of_dates):
                        try:
                            date_obj = datetime.strptime(
                                response['date_{}'.format(i)], '%d/%m/%Y')

                            start_time_obj = datetime.strptime(
                                response['start_time_{}'.format(i)], '%H:%M').time()

                            end_time_obj = datetime.strptime(
                                response['end_time_{}'.format(i)], '%H:%M').time()
                            
                            date_event = EventDates(
                                evento=old_event,
                                start_date=datetime.combine(
                                    date_obj, start_time_obj),
                                end_date=datetime.combine(date_obj, end_time_obj),
                                uso=response['type_{}'.format(i)]
                            )

                            date_event.save()
                        except:
                            print(f'Data número {i} não encontrada, indo para a p´roxima')
                        
                
                try:
                    if (request.FILES['picture__input']):
                        image_banner = True
                except:
                    image_banner = False

                if image_banner:
                    old_banner = EventImages.objects.filter(evento = old_event, is_cover=True)
                    for banner in old_banner:
                        banner.delete()

                    fss = FileSystemStorage()
                    file = request.FILES['picture__input']
                    event_image = EventImages(
                        evento=old_event,
                        image=fss.save(images_dir(old_event, file.name), file),
                        is_cover=True
                    )

                    event_image.save()

                try:
                    if (request.FILES['pictures_event_input']):
                        image_list = True
                except:
                    image_list = False

                if (image_list):
                    fss2 = FileSystemStorage()
                    for f in request.FILES.getlist('pictures_event_input'):

                        old_imgs = EventImages.objects.filter(evento = old_event, is_cover=False)
                        for img in old_imgs:
                            img.delete()

                        event_image_from_list = EventImages(
                            evento=old_event,
                            image=fss2.save(images_dir(old_event, f.name), f),
                            is_cover=False
                        )
                        event_image_from_list.save()

                messages.success(request, 'Evento atualizado com sucessp')
                return redirect('/cadastro-eventos')
            except Exception as err:
                print('erro:  '+str(err))
                messages.error(request, 'Não foi possível atualizar o evento') 
                return redirect('/cadastro-eventos')
        else:    
############### novo evento #############
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
                        try:
                            if response['date_{}'.format(i)]:
                                date_obj = datetime.strptime(
                                    response['date_{}'.format(i)], '%d/%m/%Y')

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
                        except:
                            print(f"Não foi possível encontrar a data {i}")

                fss = FileSystemStorage()
                file = request.FILES['picture__input']
                event_image = EventImages(
                    evento=event,
                    image=fss.save(images_dir(event, file.name), file),
                    is_cover=True
                )

                event_image.save()

                try:
                    if (request.FILES['pictures_event_input']):
                        image_list = True
                except:
                    image_list = False

                if (image_list):
                    fss2 = FileSystemStorage()
                    for f in request.FILES.getlist('pictures_event_input'):
                        event_image_from_list = EventImages(
                            evento=event,
                            image=fss2.save(images_dir(event, f.name), f),
                            is_cover=False
                        )
                        event_image_from_list.save()

                messages.success(request, 'Evento cadastrado com sucesso')
                return redirect('/cadastro-eventos')
            except Exception as err:
                event.delete()
                print('erro:  '+str(err))
                messages.error(request, 'Não foi possível cadastrar o evento')
                return redirect('/cadastro-eventos')    
    
    else:      
        return render(request, 'cadastroEvento.html', {'all_logged_dates': all_logged_dates})


def eventos(request):
    events = Event.objects.filter(aprovado=True)
    event_dates = EventDates.objects.filter(
        uso="AP",
        evento__in=events,
        start_date__gte=datetime.now()

    ).distinct().order_by('start_date')
    images = EventImages.objects.filter(
        is_cover=True, evento__in=events).distinct()

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

        dict.append({
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


    # event_date = EventDates.objects.all()

    # event_list = Event.objects.all().filter(
    #     usuario=request.user)


    if request.method == "POST":
        response = request.POST

        evento = Event.objects.get(pk=response["delete_event"])

        if request.user == evento.usuario: # and not evento.aprovado:
            evento.delete()
            messages.success(request, 'Evento removido com sucesso')
            return redirect('/meus-eventos')
        else:            
            messages.error(request, 'Não foi possível remover o evento')
            return redirect('/meus-eventos')

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
    

    