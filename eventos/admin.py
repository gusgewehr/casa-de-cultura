from django.contrib import admin
from .models import Event, EventDates
from django.utils.html import format_html
import datetime


# Register your models here.
class EventAdmin(admin.ModelAdmin):
    list_display = ['nome', 'get_horarios','usuario',]

    def get_horarios(self, obj):
        show_horarios = ''

        horarios = EventDates.objects.filter(evento_id = obj.id)

        
        
        for horario in horarios:
            data = horario.start_date.date().strftime('%d/%m/%y')
            inicio = horario.start_date.time().strftime('%H:%M')
            fim = horario.end_date.time().strftime('%H:%M')
            show_horarios = show_horarios + f"Dia {data} das {inicio} até {fim} <br />"
        return format_html(show_horarios)


admin.site.register(Event, EventAdmin)