from django.contrib import admin
from .models import *
# Register your models here.

class AdminCaso(admin.ModelAdmin):
	list_display = ('nombres','apellidos','cedula','departamento', 'descripcion')

class AdminReCaso(admin.ModelAdmin):
	list_display = ('caso','respuesta')

class AdminDatosUsuario(admin.ModelAdmin):
	list_display = ('usuario','departamento')

class AdminTipoCasos(admin.ModelAdmin):
	list_display = ('caso','departamento', 'descripcion', 'preguntasf')

admin.site.register(Caso, AdminCaso)
admin.site.register(ReCaso, AdminReCaso)
admin.site.register(PerfilUsuario, AdminDatosUsuario)
admin.site.register(TipoCaso, AdminTipoCasos)
