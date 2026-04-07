from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from openpyxl import Workbook

from .forms import CajaForm, TipoCajaForm
from .models import Caja, TipoCaja, UsuarioEmpresa


def login_view(request):
    if request.user.is_authenticated:
        return redirect('inicio')

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()

            try:
                usuario_empresa = user.usuario_empresa
            except UsuarioEmpresa.DoesNotExist:
                messages.error(request, 'Tu usuario no tiene una empresa asignada.')
                return redirect('login')

            if not usuario_empresa.empresa.activa:
                messages.error(request, 'La empresa asociada a este usuario está inactiva.')
                return redirect('login')

            login(request, user)
            messages.success(request, f'Bienvenido, {user.username}')
            return redirect('inicio')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'cajas/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect('login')


def obtener_empresa_usuario(request):
    return request.user.usuario_empresa.empresa


@login_required
def inicio(request):
    empresa = obtener_empresa_usuario(request)

    total_cajas = Caja.objects.filter(empresa=empresa).count()
    total_tipos = TipoCaja.objects.filter(empresa=empresa).count()
    ultimas_cajas = (
        Caja.objects
        .select_related('tipo_caja')
        .filter(empresa=empresa)
        .order_by('-id')[:5]
    )

    return render(request, 'cajas/inicio.html', {
        'empresa_actual': empresa,
        'total_cajas': total_cajas,
        'total_tipos': total_tipos,
        'ultimas_cajas': ultimas_cajas,
    })


@login_required
def listar_cajas(request):
    empresa = obtener_empresa_usuario(request)

    cajas = (
        Caja.objects
        .select_related('tipo_caja')
        .filter(empresa=empresa)
        .order_by('-id')
    )

    return render(request, 'cajas/listar_cajas.html', {
        'empresa_actual': empresa,
        'cajas': cajas
    })


@login_required
def crear_caja(request):
    empresa = obtener_empresa_usuario(request)

    if request.method == 'POST':
        form = CajaForm(request.POST, empresa=empresa)
        if form.is_valid():
            caja = form.save(commit=False)
            caja.empresa = empresa
            caja.save()
            messages.success(request, f'Se creó correctamente el código {caja.codigo}')
            return redirect('listar_cajas')
    else:
        form = CajaForm(empresa=empresa)

    return render(request, 'cajas/crear_caja.html', {
        'empresa_actual': empresa,
        'form': form
    })


@login_required
def listar_tipos_caja(request):
    empresa = obtener_empresa_usuario(request)

    tipos = TipoCaja.objects.filter(empresa=empresa).order_by('nombre')

    return render(request, 'cajas/listar_tipos_caja.html', {
        'empresa_actual': empresa,
        'tipos': tipos
    })


@login_required
def crear_tipo_caja(request):
    empresa = obtener_empresa_usuario(request)

    if request.method == 'POST':
        form = TipoCajaForm(request.POST)
        if form.is_valid():
            tipo = form.save(commit=False)
            tipo.empresa = empresa
            tipo.save()
            messages.success(request, 'Tipo de caja creado correctamente.')
            return redirect('listar_tipos_caja')
    else:
        form = TipoCajaForm()

    return render(request, 'cajas/crear_tipo_caja.html', {
        'empresa_actual': empresa,
        'form': form
    })


@login_required
def exportar_excel(request):
    empresa = obtener_empresa_usuario(request)

    wb = Workbook()
    ws = wb.active
    ws.title = "Cajas"

    ws.append([
        'Empresa',
        'Código',
        'Tipo de caja',
        'Prefijo',
        'Técnico',
        'Ubicación',
        'Descripción',
        'Fecha de creación'
    ])

    cajas = (
        Caja.objects
        .select_related('tipo_caja')
        .filter(empresa=empresa)
        .order_by('-id')
    )

    for caja in cajas:
        ws.append([
            empresa.nombre,
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
    response['Content-Disposition'] = f'attachment; filename="cajas_{empresa.nombre}.xlsx"'

    wb.save(response)
    return response


