from django.db import models

class Tarea(models.Model):
    GRADO_CHOICES = [
        ('1', 'Primer Grado'),
        ('2', 'Segundo Grado'),
        ('3', 'Tercer Grado'),
    ]

    clave = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    grado = models.CharField(max_length=1, choices=GRADO_CHOICES) 
    docente = models.CharField(max_length=100)
    fecha_entrega = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.clave} - {self.nombre}"

    class Meta:
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"

class Duda(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    mensaje = models.TextField()
    # Respuesta que el docente escribe desde el admin.
    # Si está vacía, la duda no aparece en el blog público.
    respuesta = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Duda de {self.nombre} - {self.created.strftime('%d/%m/%Y')}"

    class Meta:
        verbose_name = "Duda"
        verbose_name_plural = "Dudas"
        ordering = ['-created']