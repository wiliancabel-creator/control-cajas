from django.contrib import admin
from .models import TipoCaja, Caja


@admin.register(TipoCaja)
class TipoCajaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'prefijo', 'activo')
    search_fields = ('nombre', 'prefijo')


@admin.register(Caja)
class CajaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'tipo_caja', 'tecnico', 'ubicacion', 'fecha_creacion')
    search_fields = ('codigo', 'tecnico', 'ubicacion')
    list_filter = ('tipo_caja', 'fecha_creacion')