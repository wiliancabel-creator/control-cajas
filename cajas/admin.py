from django.contrib import admin
from .models import Empresa, UsuarioEmpresa, TipoCaja, SecuenciaCaja, Caja


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activa', 'fecha_creacion')
    search_fields = ('nombre',)


@admin.register(UsuarioEmpresa)
class UsuarioEmpresaAdmin(admin.ModelAdmin):
    list_display = ('user', 'empresa')
    search_fields = ('user__username', 'empresa__nombre')


@admin.register(TipoCaja)
class TipoCajaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'prefijo', 'empresa', 'activo')
    search_fields = ('nombre', 'prefijo', 'empresa__nombre')
    list_filter = ('empresa', 'activo')


@admin.register(SecuenciaCaja)
class SecuenciaCajaAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'tipo_caja', 'ultimo_numero')
    search_fields = ('empresa__nombre', 'tipo_caja__nombre', 'tipo_caja__prefijo')
    list_filter = ('empresa',)


@admin.register(Caja)
class CajaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'empresa', 'tipo_caja', 'tecnico', 'ubicacion', 'fecha_creacion')
    search_fields = ('codigo', 'tecnico', 'ubicacion', 'empresa__nombre')
    list_filter = ('empresa', 'tipo_caja', 'fecha_creacion')