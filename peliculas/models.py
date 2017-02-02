#encoding:utf-8
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

CHOICE_SEXO = (("M", "Male"), ("F", "Female"))


class Ocupacion(models.Model):
    nombre = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return self.nombre

class Usuario(models.Model):
    id_usuario= models.IntegerField(verbose_name="Identificador", unique=True)
    edad = models.IntegerField()
    sexo = models.CharField(max_length=1, choices=CHOICE_SEXO)
    ocupacion = models.ForeignKey(Ocupacion, verbose_name="Ocupación")
    codigo_postal = models.TextField(verbose_name="Código Postal")

    def __unicode__(self):
        return unicode(self.id_usuario)


class Categoria(models.Model):
    id_categoria = models.IntegerField()
    nombre = models.TextField(max_length=100)

    def __unicode__(self):
        return self.nombre

class Pelicula(models.Model):
    id_pelicula = models.IntegerField()
    titulo = models.TextField(verbose_name="Título")
    fecha_estreno = models.DateField()
    imdb_url = models.URLField()
    categorias = models.ManyToManyField(Categoria)

    def __unicode__(self):
        return self.titulo

class Rating(models.Model):
    usuario = models.ForeignKey(Usuario)
    pelicula = models.ForeignKey(Pelicula)
    rating = models.IntegerField(validators=[MinValueValidator(0),
                                       MaxValueValidator(5)])
    momento = models.DateTimeField()

