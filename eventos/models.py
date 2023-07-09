from datetime import timezone
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from django.forms import ValidationError



class EventManager(models.Manager):
    def get_by_natural_key(self, dict):
        return self.get(dict=dict)

# Create your models here.
class Event(models.Model):
    nome = models.CharField(max_length=500)
    descricao = models.CharField(max_length=4000)
    preco_ingresso = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    gratuito = models.BooleanField(default=False)
    ingresso_meia = models.BooleanField(default=False)
    ingresso_comunitario = models.BooleanField(default=False)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    aprovado = models.BooleanField(default=False)


    objects = EventManager()

    def natural_key(self):
        dict = {
            "id": str(self.id),
            "nome": self.nome,
            "usuario": self.usuario.get_username(),
            "aprovado": str(self.aprovado)
        }
        return (dict)

    def __str__(self):
        return self.nome
    
    def clean(self):
        event_dates = EventDates.objects.filter(evento=self.id)
        
        if event_dates:
            for date in event_dates:
                check_conflict = EventDates.objects.filter(
                            evento__aprovado=True
                        ).exclude(evento=self.id).filter( Q(start_date__gte = date.start_date, start_date__lte = date.end_date) |
                                    Q(end_date__gte = date.start_date, end_date__lte = date.end_date ) |
                                    Q(start_date__lte = date.start_date, end_date__gte = date.end_date) |
                                    Q(start_date__gte = date.start_date, end_date__lte = date.end_date)                                   
                        )[:1]
                if check_conflict:                    
                    raise ValidationError(f'Conflito de horários com {check_conflict[0]}')
    
    def save(self, *args, **kwargs):
        event_dates = EventDates.objects.filter(evento=self.id)
        
        if event_dates:
            for date in event_dates:
                check_conflict = EventDates.objects.filter(
                            evento__aprovado=True
                        ).exclude(evento=self.id).filter( Q(start_date__gte = date.start_date, start_date__lte = date.end_date) |
                                    Q(end_date__gte = date.start_date, end_date__lte = date.end_date ) |
                                    Q(start_date__lte = date.start_date, end_date__gte = date.end_date) |
                                    Q(start_date__gte = date.start_date, end_date__lte = date.end_date)                                   
                        )[:1]
                if check_conflict:
                    raise ValidationError(f'Conflito de horários com {check_conflict[0]}')


        super(Event, self).save(*args, **kwargs)
    
  

    

    

def images_dir(instance, filename):
    date = timezone.now()
    month = date.month
    if month < 10:
        month = '0' + str(month)
    return f'/imagens_eventos/{date.year}/{month}/{date.day}/{instance.evento.nome}/{filename}'


class EventDates(models.Model):
    evento = models.ForeignKey(Event, on_delete = models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    type_choices = (
        ("EN", "Ensaio"),
        ("MNT","Montagem do Palco"),
        ("AP","Apresentação"),
        ("DMNT","Desmontagem do Palco"),
    )
    uso = models.CharField(max_length=5, choices=type_choices, default="AP")

    def treat_uso(self):
        type_choices = {
            "EN": "Ensaio",
            "MNT":"Montagem do Palco",
            "AP": "Apresentação",
            "DMNT":"Desmontagem do Palco",
        }
        return type_choices[self.uso]
    
    def natural_key(self):
        return (self.id,)+self.evento.natural_key()
    
    natural_key.dependencies = ["example_app.evento"]

    def __str__(self):
        return self.evento.nome + " " + str(self.start_date)
    

    def clean(self):
        if self.start_date.date() != self.end_date.date():
            raise ValidationError('As datas de início e fim devem ocorrer no mesmo dia')

        check_conflict = EventDates.objects.filter(
            evento__aprovado=True
            ).exclude(pk=self.id).filter( Q(start_date__gte = self.start_date, start_date__lte = self.end_date) |
                                    Q(end_date__gte = self.start_date, end_date__lte = self.end_date ) |
                                    Q(start_date__lte = self.start_date, end_date__gte = self.end_date) |
                                    Q(start_date__gte = self.start_date, end_date__lte = self.end_date)                                   
                        )[:1]
        if check_conflict:
            raise ValidationError(f'Conflito de horários com {check_conflict[0]} até {check_conflict[0].end_date}')

    def save(self, *args, **kwargs):
        if self.start_date.date() != self.end_date.date():
            raise ValidationError('As datas de início e fim devem ocorrer no mesmo dia')

        check_conflict = EventDates.objects.filter(
            evento__aprovado=True
            ).exclude(pk=self.id).filter( Q(start_date__gte = self.start_date, start_date__lte = self.end_date) |
                                    Q(end_date__gte = self.start_date, end_date__lte = self.end_date ) |
                                    Q(start_date__lte = self.start_date, end_date__gte = self.end_date) |
                                    Q(start_date__gte = self.start_date, end_date__lte = self.end_date)                                   
                        )[:1]
        if check_conflict:
            raise ValidationError(f'Conflito de horários com {check_conflict[0]} até {check_conflict[0].end_date}')


        super(EventDates, self).save(*args, **kwargs)


class EventImages(models.Model):
    evento = models.ForeignKey(Event, on_delete = models.CASCADE)
    image = models.ImageField()
    is_cover = models.BooleanField(default=False)
    
