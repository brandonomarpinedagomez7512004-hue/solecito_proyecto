from django.utils import timezone
from datetime import timedelta
from .models import Tarea
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from .models import Tarea, Duda
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def inicio(request):
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

        Duda.objects.create(
            nombre=nombre,
            correo=correo,
            mensaje=mensaje,
        )
        enviado = True

    context = {'enviado': enviado}
    return render(request, 'tareas/formulario_dudas.html', context)

# Vista de login para docentes (separada del admin de Django).
# Revisa usuario y contraseña contra la base de datos y, si son
# correctos, abre sesión y manda al panel de control.

def login_docente(request):
    error = None

    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        contrasena = request.POST.get('contrasena')
        user = authenticate(request, username=usuario, password=contrasena)

        if user is not None:
            login(request, user)
            return redirect('panel_control')
        else:
            error = 'Usuario o contraseña incorrectos.'

    return render(request, 'tareas/login.html', {'error': error})


# Cierra la sesión del docente.
def logout_docente(request):
    logout(request)
    return redirect('inicio')

# Panel del docente: lista todas las tareas.
# @login_required hace que si no has iniciado sesión, te mande al login.
@login_required(login_url='login_docente')
def panel_control(request):
    tareas = Tarea.objects.all().order_by('fecha_entrega')
    return render(request, 'tareas/panel_control.html', {'tareas': tareas})


# Crea una tarea nueva a partir del formulario.
# Si es GET, solo muestra el formulario vacío.
# Si es POST, guarda los datos en la base de datos y regresa al panel.
@login_required(login_url='login_docente')
def tarea_crear(request):
    if request.method == 'POST':
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


# Edita una tarea existente (se busca por su id).
# Si es GET, muestra el formulario con los datos actuales.
# Si es POST, sobreescribe esos datos y guarda los cambios.
@login_required(login_url='login_docente')
def tarea_editar(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)

    if request.method == 'POST':
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


# Elimina una tarea, pero primero pide confirmación.
# GET = muestra la pantalla de "¿seguro?"
# POST = ya confirmado, se borra de verdad.
@login_required(login_url='login_docente')
def tarea_eliminar(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)

    if request.method == 'POST':
        tarea.delete()
        return redirect('panel_control')

    return render(request, 'tareas/tarea_confirmar_eliminar.html', {'tarea': tarea})


# Blog público de dudas ya respondidas.
# Solo muestra las dudas donde el campo "respuesta" no está vacío.
def blog_dudas(request):
    dudas = Duda.objects.exclude(respuesta__isnull=True).exclude(respuesta='').order_by('-created')
    return render(request, 'tareas/blog_dudas.html', {'dudas': dudas})


# Página estática con información de contacto del jardín.
def acerca(request):
    return render(request, 'tareas/acerca.html')