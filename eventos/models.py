from datetime import timezone
from django.db import models
from django.contrib.auth.models import User



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


class EventImages(models.Model):
    evento = models.ForeignKey(Event, on_delete = models.CASCADE)
    image = models.ImageField()
    is_cover = models.BooleanField(default=False)
    
