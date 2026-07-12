from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('tarea/<int:tarea_id>/', views.detalle, name='detalle'),
    path('dudas/', views.formulario_dudas, name='formulario_dudas'),
    path('blog-dudas/', views.blog_dudas, name='blog_dudas'),
    path('acerca/', views.acerca, name='acerca'),
    path('login/', views.login_docente, name='login_docente'),
    path('logout/', views.logout_docente, name='logout_docente'),
    path('panel/', views.panel_control, name='panel_control'),
    path('panel/tarea/nueva/', views.tarea_crear, name='tarea_crear'),
    path('panel/tarea/<int:tarea_id>/editar/', views.tarea_editar, name='tarea_editar'),
    path('panel/tarea/<int:tarea_id>/eliminar/', views.tarea_eliminar, name='tarea_eliminar'),
]