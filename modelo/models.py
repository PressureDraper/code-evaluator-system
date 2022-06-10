from operator import truediv
from pydoc import describe
from django.db import models

# Create your models here.
class users(models.Model):
    name = models.CharField(max_length=30, null=False)
    email = models.EmailField(max_length=254, null=False)
    reason = models.CharField(max_length=254, unique=True, null=False)
    use = models.CharField(max_length=254, null=False)
    date = models.CharField(max_length=30, null=False)
    hour = models.CharField(max_length=30, null=False)
    phone = models.BigIntegerField(null=False)

class testing(models.Model):
    username = models.CharField(max_length=30, null=False)
    pwd = models.CharField(max_length=30, null=False)

class testfiles(models.Model):
    title = models.CharField(max_length = 200)
    uploaded = models.FileField(upload_to = "upload/")
    date = models.DateTimeField(auto_now = True)

class maestros(models.Model):
    usuario = models.CharField(max_length = 50)
    email = models.EmailField(max_length=254, null=False)
    passwd = models.CharField(max_length=254, null=False)

class alumnos(models.Model):
    idMaestro = models.ForeignKey(maestros, on_delete=models.CASCADE, null=True)
    nombre = models.CharField(max_length = 254, blank=True)
    usuario = models.CharField(max_length = 50)
    email = models.EmailField(max_length=254, null=False)
    passwd = models.CharField(max_length=254, null=False)

class grupo(models.Model):
    idMaestro = models.ForeignKey(maestros, on_delete=models.CASCADE, null=True)
    asignatura = models.CharField(max_length = 254, blank=True)
    turno = models.CharField(max_length = 254, blank=True)
    initDate = models.CharField(max_length=60, null=False)
    finalDate = models.CharField(max_length=60, null=False)

class ejercicios(models.Model):
    idMaestro = models.ForeignKey(maestros, on_delete=models.CASCADE)
    titulo = models.CharField(max_length = 254)
    descripcion = models.CharField(max_length = 254)
    fecha = models.DateTimeField(auto_now = True)
    sInicializacion = models.FileField(upload_to = "upload/maestro", blank=True)
    sEntradas = models.FileField(upload_to = "upload/maestro", blank=True)
    sSalida = models.FileField(upload_to = "upload/maestro", blank=True)
    sParametros = models.FileField(upload_to = "upload/maestro", blank=True)
    sEdoFinal = models.FileField(upload_to = "upload/maestro", blank=True)
    visible = models.BooleanField(default=False)

class evaluaciones(models.Model):
    idEjercicio = models.ForeignKey(ejercicios, on_delete=models.CASCADE)
    idAlumno = models.ForeignKey(alumnos, on_delete=models.CASCADE)
    script = models.FileField(upload_to = "upload/alumno", blank=True)
    resultado = models.CharField(max_length = 254, blank=True)
    calificacion = models.IntegerField(blank=True, null=True)
    intentos = models.IntegerField(blank=True, null=True)