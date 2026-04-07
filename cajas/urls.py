from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('cajas/', views.listar_cajas, name='listar_cajas'),
    path('cajas/crear/', views.crear_caja, name='crear_caja'),
    path('tipos-caja/', views.listar_tipos_caja, name='listar_tipos_caja'),
    path('tipos-caja/crear/', views.crear_tipo_caja, name='crear_tipo_caja'),
    path('exportar/excel/', views.exportar_excel, name='exportar_excel'),
]