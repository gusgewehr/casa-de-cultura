from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Event(models.Model):
    nome = models.CharField(max_length=500)
    descricao = models.CharField(max_length=4000)
    preco_ingresso = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    gratuito = models.BooleanField(default=False)
    ingresso_meia = models.BooleanField(default=False)
    ingresso_comunitario = models.BooleanField(default=False)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)




class EventDates(models.Model):
    evento = models.ForeignKey(Event, on_delete = models.CASCADE)
    date = models.DateTimeField()
    type_choices = (
        ("EN", "Ensaio"),
        ("MNT","Montagem do Palco"),
        ("AP","Apresentação"),
        ("DMNT","Desmontagem do Palco"),
    )
    uso = models.CharField(max_length=5, choices=type_choices, default="AP")
