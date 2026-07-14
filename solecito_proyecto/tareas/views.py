from django.utils import timezone
from datetime import timedelta
from .models import Tarea
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from .models import Tarea, Duda
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def inicio(request):
    # Obtiene el grado seleccionado desde la URL para filtrar las tareas
    grado_seleccionado = request.GET.get('grado')

    if grado_seleccionado:
        tareas_qs = Tarea.objects.filter(grado=grado_seleccionado)
    else:
        tareas_qs = Tarea.objects.all()

    tareas_qs = tareas_qs.order_by('fecha_entrega')

    hoy = timezone.now().date()
    tareas = []

    for tarea in tareas_qs:
        dias_restantes = (tarea.fecha_entrega - hoy).days

        # Asigna un color según la cercanía de la fecha de entrega
        if dias_restantes <= 1:
            urgencia = 'rojo'
        elif dias_restantes <= 4:
            urgencia = 'amarillo'
        else:
            urgencia = 'verde'

        tareas.append({
            'obj': tarea,
            'dias_restantes': dias_restantes,
            'urgencia': urgencia,
        })

    context = {
        'tareas': tareas,
        'grado_seleccionado': grado_seleccionado,
    }
    return render(request, 'tareas/inicio.html', context)


def detalle(request, tarea_id):
    # Busca la tarea por su id o muestra error 404 si no existe
    tarea = get_object_or_404(Tarea, id=tarea_id)

    hoy = timezone.now().date()
    dias_restantes = (tarea.fecha_entrega - hoy).days

    if dias_restantes <= 1:
        urgencia = 'rojo'
    elif dias_restantes <= 4:
        urgencia = 'amarillo'
    else:
        urgencia = 'verde'

    context = {
        'tarea': tarea,
        'dias_restantes': dias_restantes,
        'urgencia': urgencia,
    }
    return render(request, 'tareas/detalle.html', context)


def formulario_dudas(request):
    enviado = False

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        mensaje = request.POST.get('mensaje')

        # Guarda la duda enviada por el usuario
        Duda.objects.create(
            nombre=nombre,
            correo=correo,
            mensaje=mensaje,
        )
        enviado = True

    context = {'enviado': enviado}
    return render(request, 'tareas/formulario_dudas.html', context)


def login_docente(request):
    error = None

    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        contrasena = request.POST.get('contrasena')
        user = authenticate(request, username=usuario, password=contrasena)

        # Verifica las credenciales del docente
        if user is not None:
            login(request, user)
            return redirect('panel_control')
        else:
            error = 'Usuario o contraseña incorrectos.'

    return render(request, 'tareas/login.html', {'error': error})


def logout_docente(request):
    logout(request)
    return redirect('inicio')


# Solo usuarios autenticados pueden acceder al panel
@login_required(login_url='login_docente')
def panel_control(request):
    tareas = Tarea.objects.all().order_by('fecha_entrega')
    return render(request, 'tareas/panel_control.html', {'tareas': tareas})


@login_required(login_url='login_docente')
def tarea_crear(request):
    if request.method == 'POST':
        # Crea una nueva tarea con los datos del formulario
        Tarea.objects.create(
            clave=request.POST.get('clave'),
            nombre=request.POST.get('nombre'),
            descripcion=request.POST.get('descripcion'),
            grado=request.POST.get('grado'),
            docente=request.POST.get('docente'),
            fecha_entrega=request.POST.get('fecha_entrega'),
        )
        return redirect('panel_control')

    context = {'tarea': None, 'grados': Tarea.GRADO_CHOICES}
    return render(request, 'tareas/tarea_form.html', context)


@login_required(login_url='login_docente')
def tarea_editar(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)

    if request.method == 'POST':
        # Actualiza la información de la tarea seleccionada
        tarea.clave = request.POST.get('clave')
        tarea.nombre = request.POST.get('nombre')
        tarea.descripcion = request.POST.get('descripcion')
        tarea.grado = request.POST.get('grado')
        tarea.docente = request.POST.get('docente')
        tarea.fecha_entrega = request.POST.get('fecha_entrega')
        tarea.save()
        return redirect('panel_control')

    context = {'tarea': tarea, 'grados': Tarea.GRADO_CHOICES}
    return render(request, 'tareas/tarea_form.html', context)


@login_required(login_url='login_docente')
def tarea_eliminar(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)

    if request.method == 'POST':
        # Elimina la tarea de la base de datos
        tarea.delete()
        return redirect('panel_control')

    return render(request, 'tareas/tarea_confirmar_eliminar.html', {'tarea': tarea})


def blog_dudas(request):
    # Muestra únicamente las dudas que ya tienen respuesta
    dudas = Duda.objects.exclude(respuesta__isnull=True).exclude(respuesta='').order_by('-created')
    return render(request, 'tareas/blog_dudas.html', {'dudas': dudas})


def acerca(request):
    return render(request, 'tareas/acerca.html')