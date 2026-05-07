from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Sum

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Vehiculo, Operario, Mantencion, Faena, RegistroIncidente
from .forms import VehiculoForm, OperarioForm, FaenaForm
from datetime import date
import logging

logger = logging.getLogger(__name__)

# ===== AUTENTICACIÓN =====
def login_view(request):
    """Vista de inicio de sesión"""
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido {user.username}!')
            next_url = request.GET.get('next', 'index')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    
    return render(request, 'registration/login.html')


def logout_view(request):
    """Vista de cierre de sesión"""
    logout(request)
    messages.info(request, 'Sesión cerrada exitosamente.')
    return redirect('login')


def register_view(request):
    """Vista de registro de nuevos usuarios"""
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Validaciones
        if not username or not password1:
            messages.error(request, 'Usuario y contraseña son requeridos.')
        elif password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
        elif len(password1) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe.')
        else:
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1
                )
                login(request, user)
                messages.success(request, 'Cuenta creada exitosamente!')
                return redirect('index')
            except Exception as e:
                logger.error(f'Error al crear usuario: {str(e)}')
                messages.error(request, 'Error al crear la cuenta.')
    
    return render(request, 'registration/register.html')

@login_required
def index(request):
    """Vista principal con dashboard forestal"""
    vehiculos_count = Vehiculo.objects.filter(estado='operativo').count()
    operarios_count = Operario.objects.filter(activo=True).count()
    faenas_count = Faena.objects.count()
    mantenciones_pendientes = Mantencion.objects.filter(estado='programada').count()
    
    # Estadísticas Globales
    produccion_total = Faena.objects.aggregate(Sum('metros_cubicos'))['metros_cubicos__sum'] or 0
    costo_mantencion = Mantencion.objects.aggregate(Sum('costo'))['costo__sum'] or 0
    
    # Faenas recientes
    faenas_recientes = Faena.objects.select_related('vehiculo', 'operario').order_by('-fecha_creacion')[:5]
    
    # Faenas activas
    faenas_activas = Faena.objects.filter(estado='en_curso').select_related('vehiculo', 'operario')[:5]
    
    # Mantenciones próximas
    mantenciones_proximas = Mantencion.objects.filter(
        estado='programada',
        fecha_programada__gte=date.today()
    ).select_related('vehiculo').order_by('fecha_programada')[:5]
    
    # Vehículos en mantención
    vehiculos_mantencion = Vehiculo.objects.filter(estado='mantencion').order_by('-horas_uso')[:5]
    
    # Incidentes Recientes
    incidentes_recientes = RegistroIncidente.objects.select_related('faena').order_by('-fecha_incidente')[:5]
    
    context = {
        'vehiculos_count': vehiculos_count,
        'operarios_count': operarios_count,
        'faenas_count': faenas_count,
        'mantenciones_pendientes': mantenciones_pendientes,
        'produccion_total': produccion_total,
        'costo_mantencion': costo_mantencion,
        'faenas_recientes': faenas_recientes,
        'faenas_activas': faenas_activas,
        'mantenciones_proximas': mantenciones_proximas,
        'vehiculos_mantencion': vehiculos_mantencion,
        'incidentes_recientes': incidentes_recientes,
    }
    return render(request, 'entregables/index.html', context)


# ===== CRUD VEHÍCULOS =====
@login_required
def vehiculo_list(request):
    """Lista de vehículos"""
    vehiculos = Vehiculo.objects.all().order_by('-fecha_creacion')
    busqueda = request.GET.get('q')
    estado_filter = request.GET.get('estado')
    
    if busqueda:
        vehiculos = vehiculos.filter(
            Q(patente__icontains=busqueda) | 
            Q(marca__icontains=busqueda) |
            Q(modelo__icontains=busqueda)
        )
    if estado_filter:
        vehiculos = vehiculos.filter(estado=estado_filter)
    
    context = {
        'vehiculos': vehiculos,
        'busqueda': busqueda,
        'estado_filter': estado_filter,
        'estados': Vehiculo.ESTADOS,
        'title': 'Gestión de Vehículos'
    }
    return render(request, 'entregables/vehiculo_list.html', context)


@login_required
def vehiculo_create(request):
    """Crear nuevo vehículo usando ModelForm"""
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehículo registrado exitosamente.')
            return redirect('vehiculo_list')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = VehiculoForm()
    
    context = {
        'form': form,
        'title': 'Registrar Nuevo Vehículo',
        'back_url': 'vehiculo_list'
    }
    return render(request, 'entregables/vehiculo_form.html', context)


@login_required
def vehiculo_update(request, pk):
    """Actualizar vehículo usando ModelForm"""
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    
    if request.method == 'POST':
        form = VehiculoForm(request.POST, instance=vehiculo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehículo actualizado exitosamente.')
            return redirect('vehiculo_list')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = VehiculoForm(instance=vehiculo)
    
    context = {
        'form': form,
        'title': f'Editar Vehículo: {vehiculo.patente}',
        'back_url': 'vehiculo_list'
    }
    return render(request, 'entregables/vehiculo_form.html', context)


@login_required
def vehiculo_delete(request, pk):
    """Eliminar vehículo"""
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    if request.method == 'POST':
        vehiculo.delete()
        messages.success(request, 'Vehículo eliminado exitosamente.')
        return redirect('vehiculo_list')
    
    context = {
        'object': vehiculo,
        'title': 'Eliminar Vehículo',
        'back_url': 'vehiculo_list'
    }
    return render(request, 'entregables/vehiculo_confirm_delete.html', context)


# ===== CRUD OPERARIOS =====
@login_required
def operario_list(request):
    """Lista de operarios"""
    operarios = Operario.objects.all().order_by('nombre')
    context = {
        'operarios': operarios,
        'title': 'Gestión de Operarios'
    }
    return render(request, 'entregables/operario_list.html', context)


@login_required
def operario_create(request):
    """Crear nuevo operario usando ModelForm"""
    if request.method == 'POST':
        form = OperarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Operario registrado exitosamente.')
            return redirect('operario_list')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = OperarioForm()
    
    context = {
        'form': form,
        'title': 'Registrar Nuevo Operario',
        'back_url': 'operario_list'
    }
    return render(request, 'entregables/operario_form.html', context)


@login_required
def operario_update(request, pk):
    """Actualizar operario usando ModelForm"""
    operario = get_object_or_404(Operario, pk=pk)
    
    if request.method == 'POST':
        form = OperarioForm(request.POST, instance=operario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Operario actualizado exitosamente.')
            return redirect('operario_list')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = OperarioForm(instance=operario)
    
    context = {
        'form': form,
        'title': f'Editar Operario: {operario.nombre}',
        'back_url': 'operario_list'
    }
    return render(request, 'entregables/operario_form.html', context)


@login_required
def operario_delete(request, pk):
    """Eliminar operario"""
    operario = get_object_or_404(Operario, pk=pk)
    
    if request.method == 'POST':
        try:
            operario.delete()
            messages.success(request, 'Operario eliminado exitosamente.')
            return redirect('operario_list')
        except Exception as e:
            logger.error(f'Error al eliminar operario: {str(e)}')
            messages.error(request, 'Error al eliminar operario.')
    
    context = {'operario': operario}
    return render(request, 'entregables/operario_confirm_delete.html', context)


# ===== CRUD FAENAS =====
@login_required
def faena_list(request):
    """Lista de faenas"""
    faenas = Faena.objects.select_related('vehiculo', 'operario').order_by('-fecha_inicio')
    estado_filter = request.GET.get('estado')
    tipo_filter = request.GET.get('tipo')
    busqueda = request.GET.get('q')
    
    if estado_filter:
        faenas = faenas.filter(estado=estado_filter)
    if tipo_filter:
        faenas = faenas.filter(tipo=tipo_filter)
    if busqueda:
        faenas = faenas.filter(
            Q(nombre__icontains=busqueda) | 
            Q(ubicacion__icontains=busqueda)
        )
    
    context = {
        'faenas': faenas,
        'busqueda': busqueda,
        'estado_filter': estado_filter,
        'tipo_filter': tipo_filter,
        'estados': Faena.ESTADOS,
        'tipos': Faena.TIPOS,
        'title': 'Gestión de Faenas'
    }
    return render(request, 'entregables/faena_list.html', context)


@login_required
def faena_create(request):
    """Crear nueva faena"""
    if request.method == 'POST':
        try:
            nombre = request.POST.get('nombre')
            if not nombre:
                raise ValueError('El nombre de la faena es requerido')
            
            Faena.objects.create(
                nombre=nombre,
                tipo=request.POST.get('tipo'),
                ubicacion=request.POST.get('ubicacion'),
                vehiculo_id=request.POST.get('vehiculo'),
                operario_id=request.POST.get('operario') or None,
                estado=request.POST.get('estado', 'planificada'),
                fecha_inicio=request.POST.get('fecha_inicio'),
                fecha_termino=request.POST.get('fecha_termino') or None,
                metros_cubicos=request.POST.get('metros_cubicos') or None,
                hectareas=request.POST.get('hectareas') or None,
                observaciones=request.POST.get('observaciones', '')
            )
            messages.success(request, 'Faena creada exitosamente.')
            return redirect('faena_list')
            
        except ValueError as e:
            messages.error(request, f'Error: {str(e)}')
        except Exception as e:
            logger.error(f'Error al crear faena: {str(e)}')
            messages.error(request, 'Error al crear faena.')
    
    vehiculos = Vehiculo.objects.filter(estado='operativo')
    operarios = Operario.objects.filter(activo=True)
    
    context = {
        'action': 'Crear',
        'vehiculos': vehiculos,
        'operarios': operarios,
        'tipos': Faena.TIPOS,
        'estados': Faena.ESTADOS
    }
    return render(request, 'entregables/faena_form.html', context)


@login_required
def faena_update(request, pk):
    """Actualizar faena"""
    faena = get_object_or_404(Faena, pk=pk)
    
    if request.method == 'POST':
        try:
            faena.nombre = request.POST.get('nombre')
            faena.tipo = request.POST.get('tipo')
            faena.ubicacion = request.POST.get('ubicacion')
            faena.vehiculo_id = request.POST.get('vehiculo')
            faena.operario_id = request.POST.get('operario') or None
            faena.estado = request.POST.get('estado')
            faena.fecha_inicio = request.POST.get('fecha_inicio')
            faena.fecha_termino = request.POST.get('fecha_termino') or None
            faena.metros_cubicos = request.POST.get('metros_cubicos') or None
            faena.hectareas = request.POST.get('hectareas') or None
            faena.observaciones = request.POST.get('observaciones', '')
            
            faena.save()
            messages.success(request, 'Faena actualizada exitosamente.')
            return redirect('faena_list')
            
        except Exception as e:
            logger.error(f'Error al actualizar faena: {str(e)}')
            messages.error(request, 'Error al actualizar faena.')
    
    vehiculos = Vehiculo.objects.all()
    operarios = Operario.objects.filter(activo=True)
    
    context = {
        'faena': faena,
        'action': 'Actualizar',
        'vehiculos': vehiculos,
        'operarios': operarios,
        'tipos': Faena.TIPOS,
        'estados': Faena.ESTADOS
    }
    return render(request, 'entregables/faena_form.html', context)


@login_required
def faena_delete(request, pk):
    """Eliminar faena"""
    faena = get_object_or_404(Faena, pk=pk)
    
    if request.method == 'POST':
        try:
            faena.delete()
            messages.success(request, 'Faena eliminada exitosamente.')
            return redirect('faena_list')
        except Exception as e:
            logger.error(f'Error al eliminar faena: {str(e)}')
            messages.error(request, 'Error al eliminar faena.')
    
    context = {'faena': faena}
    return render(request, 'entregables/faena_confirm_delete.html', context)


@login_required
def faena_detail(request, pk):
    """Detalle de faena con incidentes"""
    faena = get_object_or_404(Faena, pk=pk)
    incidentes = faena.incidentes.all()
    
    if request.method == 'POST':
        try:
            RegistroIncidente.objects.create(
                faena=faena,
                tipo=request.POST.get('tipo'),
                gravedad=request.POST.get('gravedad'),
                descripcion=request.POST.get('descripcion'),
                medidas_tomadas=request.POST.get('medidas_tomadas', ''),
                reportado_por=request.POST.get('reportado_por')
            )
            messages.success(request, 'Incidente registrado exitosamente.')
            return redirect('faena_detail', pk=pk)
        except Exception as e:
            logger.error(f'Error al registrar incidente: {str(e)}')
            messages.error(request, 'Error al registrar incidente.')
    
    context = {
        'faena': faena,
        'incidentes': incidentes,
        'tipos_incidente': RegistroIncidente.TIPOS,
        'gravedades': RegistroIncidente.GRAVEDAD
    }
    return render(request, 'entregables/faena_detail.html', context)
