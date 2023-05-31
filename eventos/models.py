from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html



# Create your models here.
class Event(models.Model):
    nome = models.CharField(max_length=500)
    descricao = models.CharField(max_length=4000)
    preco_ingresso = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    gratuito = models.BooleanField(default=False)
    ingresso_meia = models.BooleanField(default=False)
    ingresso_comunitario = models.BooleanField(default=False)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    

    def get_horarios(self, obj):
        show_horarios = ''

        horarios = EventDates.objects.filter(evento_id = obj.id)

        
        
        for horario in horarios:
            show_horarios = show_horarios + f"Dia {horario.start_date.date()} das {horario.start_date.time()} até {horario.end_date.time()}; <br />"
        return format_html(show_horarios)



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
