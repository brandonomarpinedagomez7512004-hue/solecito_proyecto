from django.contrib import admin
from .models import Tarea,Duda

class TareaAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('clave', 'nombre', 'grado', 'docente', 'fecha_entrega')
    search_fields = ('clave', 'nombre', 'docente')
    list_filter = ('grado', 'fecha_entrega')
    date_hierarchy = 'fecha_entrega'
    list_display_links = ('clave', 'nombre')
    list_per_page = 10

admin.site.register(Tarea, TareaAdmin)

class DudaAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)
    list_display = ('nombre', 'correo', 'created', 'respondida')
    search_fields = ('nombre', 'correo')
    date_hierarchy = 'created'
    list_per_page = 10

# Muestra una palomita/tache en la lista del admin
    # según si la duda ya tiene respuesta o no.
    def respondida(self, obj):
        return bool(obj.respuesta)
    respondida.boolean = True

admin.site.register(Duda, DudaAdmin)