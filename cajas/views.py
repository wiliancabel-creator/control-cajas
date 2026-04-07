from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from openpyxl import Workbook

from .forms import CajaForm, TipoCajaForm
from .models import Caja, TipoCaja


def inicio(request):
    total_cajas = Caja.objects.count()
    total_tipos = TipoCaja.objects.count()
    ultimas_cajas = Caja.objects.select_related('tipo_caja').order_by('-id')[:5]

    return render(request, 'cajas/inicio.html', {
        'total_cajas': total_cajas,
        'total_tipos': total_tipos,
        'ultimas_cajas': ultimas_cajas,
    })


def listar_cajas(request):
    cajas = Caja.objects.select_related('tipo_caja').all()
    return render(request, 'cajas/listar_cajas.html', {
        'cajas': cajas
    })


def crear_caja(request):
    if request.method == 'POST':
        form = CajaForm(request.POST)
        if form.is_valid():
            caja = form.save()
            messages.success(request, f'Se creó correctamente el código {caja.codigo}')
            return redirect('listar_cajas')
    else:
        form = CajaForm()

    return render(request, 'cajas/crear_caja.html', {
        'form': form
    })


def listar_tipos_caja(request):
    tipos = TipoCaja.objects.all()
    return render(request, 'cajas/listar_tipos_caja.html', {
        'tipos': tipos
    })


def crear_tipo_caja(request):
    if request.method == 'POST':
        form = TipoCajaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de caja creado correctamente.')
            return redirect('listar_tipos_caja')
    else:
        form = TipoCajaForm()

    return render(request, 'cajas/crear_tipo_caja.html', {
        'form': form
    })


def exportar_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Cajas"

    ws.append([
        'Código',
        'Tipo de caja',
        'Prefijo',
        'Técnico',
        'Ubicación',
        'Descripción',
        'Fecha de creación'
    ])

    cajas = Caja.objects.select_related('tipo_caja').all()

    for caja in cajas:
        ws.append([
            caja.codigo,
            caja.tipo_caja.nombre,
            caja.tipo_caja.prefijo,
            caja.tecnico or '',
            caja.ubicacion or '',
            caja.descripcion or '',
            caja.fecha_creacion.strftime('%d/%m/%Y %H:%M')
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="cajas.xlsx"'

    wb.save(response)
    return response


