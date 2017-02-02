#encoding:utf-8
# Create your views here.
import os
from datetime import datetime, date
from django.forms import forms

from django.db import IntegrityError
from django.shortcuts import render_to_response
from django.conf import settings
from peliculas.forms import FormCategoria
from peliculas.forms import peliculasform
from peliculas.models import Categoria, Ocupacion, Usuario, Pelicula, Rating


def formularioCategoria(request):
    formulario = FormCategoria()

    return render_to_response('formCategoria.html', {'formulario': formulario})


def index(request):
    return render_to_response('index.html')


def lista_categorias(param):
    cont = 0
    categorias = []
    while cont < len(param):
        if param[cont] != '0':
            c = Categoria.objects.get(pk=cont+1)
            if c !=None:
                categorias.append(c)
        cont += 1

    return categorias



def cargar(request):
    cont = 0

    datos = open(os.path.join(settings.PROJECT_ROOT, '../peliculas/static/categorias.data'), 'r')
    for linea in datos:
        linea = linea[:-1]
        Categoria.objects.create(id_categoria = cont, nombre = linea)
        cont += 1

    datos = open(os.path.join(settings.PROJECT_ROOT, '../peliculas/static/u.occupation'), 'r')
    for linea in datos:
        linea = linea[:-1]
        Ocupacion.objects.create(nombre=linea)

    datos = open(os.path.join(settings.PROJECT_ROOT, '../peliculas/static/u.user'), 'r')
    for linea in datos:
        campos = linea.split('|')
        id_usuario = int(campos[0])
        edad = int(campos[1])

        sexo = campos[2]

        ocupacion = Ocupacion.objects.get(nombre__contains=campos[3])
        ocupacion = ocupacion
        postal = campos[4]
        postal = postal[:-1]
        Usuario.objects.create(id_usuario = id_usuario, edad = edad, sexo = sexo, ocupacion = ocupacion, codigo_postal = postal)

    datos = open(os.path.join(settings.PROJECT_ROOT, '../peliculas/static/u.item'), 'r')
    dict = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct":10,
        "Nov":11,
        "Dec":12
    }
    for linea in datos:
        campos = linea.split('|')
        id_pelicula = int(campos[0])
        titulo = campos[1]
        fecha_estreno = datetime.strptime(campos[2], "%d-%b-%Y")
        fecha = campos[2].split('-')
        dia = int(fecha[0])
        mes = dict[fecha[1]]
        ano = int(fecha[2])
        fecha = date(ano, mes, dia)
        imdb_url = campos[4]
        try:
            p = Pelicula.objects.create(id_pelicula=id_pelicula, titulo=titulo, fecha_estreno=fecha, imdb_url=imdb_url)
            categorias = lista_categorias(campos[5:19])

            for elem in categorias:
                p.categorias.add(elem)
                p.save()
        except:
            pass



    datos = open(os.path.join(settings.PROJECT_ROOT, '../peliculas/static/u.data'), 'r')
    for linea in datos:
        campos = linea.split('\t')
        id_usuario = int(campos[0])
        id_pelicula = int(campos[1])
        rating = int(campos[2])
        momento = datetime.fromtimestamp(int(campos[3]))
        usuario = Usuario.objects.get(id_usuario = id_usuario)
        try:
            pelicula = Pelicula.objects.get(id_pelicula = id_pelicula)
            if pelicula!=None and usuario!=None:
                Rating.objects.create(usuario = usuario, pelicula = pelicula, rating = rating, momento = momento)
        except:
            pass
    return render_to_response('index.html')


def peliculas(request):
    querySet = Pelicula.objects.all()
    return render_to_response('peliculas.html', {'querySet': querySet})


def categorias(request):
    querySet = Categoria.objects.all()
    return render_to_response('categorias.html', {'querySet': querySet})


def usuarios_por_postal(request):
    codigos = Usuario.objects.values('codigo_postal')
    l = []

    for elem in codigos:
        for k,v in elem.iteritems():
            dict = {}
            dict[v] = Usuario.objects.filter(codigo_postal=v)
            l.append(dict)

    return render_to_response('usuarios_por_postal.html', {'resultados' : l})


def usuarios_por_ocupacion(request):
    ocupaciones = Ocupacion.objects.values('nombre')
    l = []
    for elem in ocupaciones:
        for k,v in elem.iteritems():
            dict = {}
            ocupacion = Ocupacion.objects.filter(nombre=v)
            dict[v] = Usuario.objects.filter(ocupacion = ocupacion)
            l.append(dict)

    return render_to_response('usuarios_por_ocupacion.html', {'resultados':l})

def pelicula_detalle(request, id_pelicula):
    p = None
    try:
        p = Pelicula.objects.get(id_pelicula=id_pelicula)
        ratings = Rating.objects.filter(pelicula=p)
        media = 0
        for rating in ratings:
            media += rating.rating
        media = media/len(ratings)

        return render_to_response('pelicula_detalle.html', {'pelicula': p, 'ratings':ratings, 'media': media} )
    except:
        return render_to_response('pelicula_detalle.html', {'pelicula': p})


def peliculas_mejor_puntuadas(request):
    querySet = Rating.objects.values('pelicula')
    dict = {}
    for elem in querySet:
        list = []
        for k, v in elem.iteritems():
            list.append(Rating.objects.filter(pelicula=v))
        dict[v] = list
    titulos = []
    for elem in dict:
        media = 0.0
        for ratins in dict[elem]:
            for ratin in ratins:
                media += ratin.rating
            media = media / len(ratins)
        titulo = Pelicula.objects.filter(id_pelicula=elem)
        tit = str(titulo)
        titulo = tit + "      Puntuacion:  " + str(media)
        titulos.append(titulo)

    return render_to_response('peliculas_mejor_puntuadas.html', {'querySet': titulos})

#     try:
#         querySet = Pelicula.objects.all()
#         for peli in peliculas:
#             id = Pelicula.objects.filter(titulo = peli.titulo)
#             ratings = Rating.objects.filter(pelicula_id = id)
#             media = 0
#             for rating in ratings:
#                 media += rating.rating
#             media = media/len(ratings)
#
#         return render_to_response('peliculas_mejor_puntuadas.html', {'pelicula': querySet, 'ratings': ratings, 'media': media})
#     except:
#         return render_to_response('peliculas_mejor_puntuadas.html', {'pelicula': querySet})
#
#     return render_to_response('peliculas_mejor_puntuadas.html', {'querySet': querySet})

def peliculasform(request):
    formulario = peliculasform
    return render_to_response('peliculasform.html', {'formulario': formulario})