from django.db import models

# Create your models here.
class Evento(models.Model):
    nome = models.CharField(max_length=500)
    descricao = models.CharField(max_length=4000)
    preco_ingresso = models.DecimalField(decimal_places=2)
    ingresso_meia = models.BooleanField()
    ingresso_comunitario = models.BooleanField()

class EventDates(models.Model):
    evento = models.ForeignKey(Evento, on_delete = models.CASCADE)
    date = models.DateTimeField()
    type_choices = (
        ("EN", "Ensaio"),
        ("MNT","Montagem do Palco"),
        ("AP","Apresentação"),
        ("DMNT","Desmontagem do Palco"),
    )
    uso = models.CharField(max_length=5, choices=type_choices, default="AP")



