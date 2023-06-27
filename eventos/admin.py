from django.contrib import admin
from .models import Event, EventDates, EventImages
from django.utils.html import format_html
import datetime



class EventDatesInline(admin.TabularInline):
    model = EventDates
    extra = 0

class EventImagesInline(admin.TabularInline):
    model = EventImages
    extra = 0


# Register your models here.
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['nome', 'get_horarios','usuario', 'aprovado']
    search_fields = ('nome','usuario')
    list_editable=['aprovado']

    def get_horarios(self, obj):
        show_horarios = ''

        horarios = EventDates.objects.filter(evento_id = obj.id)

        for horario in horarios:
            data = horario.start_date.date().strftime('%d/%m/%y')
            inicio = horario.start_date.time().strftime('%H:%M')
            fim = horario.end_date.time().strftime('%H:%M')
            show_horarios = show_horarios + f"Dia {data} das {inicio} até {fim} <br />"
        return format_html(show_horarios)
    
    # def aprovar(self, obj):
    #     yes_icon = '<img src="/static/admin/img/icon-yes.svg" alt="True">'
    #     no_icon = '<img src="/static/admin/img/icon-no.svg" alt="False">'

    #     #obj.aprovado = not obj.aprovado
    #     #obj.save()

    #     if obj.aprovado:
    #         return format_html('<a href="">%s</a>' % yes_icon)
    #     else:
    #         return format_html('<a href="">%s</a>' % no_icon)

    # aprovar.short_description = 'Aprovar'

    inlines = [EventDatesInline, EventImagesInline]

    