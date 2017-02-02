#encoding:utf-8
from django.forms import ModelForm
from django import forms

from peliculas.models import Categoria,Pelicula


class FormCategoria(ModelForm):
    class Meta:
        model = Categoria

class peliculasform(ModelForm):
    class Meta:
        model = Pelicula