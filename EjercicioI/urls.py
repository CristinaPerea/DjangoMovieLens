from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'EjercicioI.views.home', name='home'),
    # url(r'^EjercicioI/', include('EjercicioI.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^formularioCategoria/$', 'peliculas.views.formularioCategoria', name="formCategoria"),
    url(r'^$', 'peliculas.views.index', name = "index"),
    url(r'^cargar/$', 'peliculas.views.cargar', name = "cargar"),
    url(r'^peliculas/$', 'peliculas.views.peliculas', name = "peliculas"),
    url(r'^peliculas/(?P<id_pelicula>\d+)$', 'peliculas.views.pelicula_detalle', name = "peliculasDetalle"),
    url(r'^categorias/$', 'peliculas.views.categorias', name = "categorias"),
    url(r'^usuarios_por_postal/$', 'peliculas.views.usuarios_por_postal', name = "usuarios_por_postal"),
    url(r'^usuarios_por_ocupacion/$', 'peliculas.views.usuarios_por_ocupacion', name = "usuarios_por_ocupacion"),
    url(r'^peliculas_mejor_puntuadas/$', 'peliculas.views.peliculas_mejor_puntuadas', name = "peliculas_mejor_puntuadas"),
    url(r'^peliculasform/$', 'peliculas.views.peliculasform', name = "peliculasform"),
    url(r'^pelicula_mas_likes/$', 'peliculas.views.pelicula_mas_likes', name= "pelicula_mas_likes"),
    url(r'^peliculas_por_lenguaje/$', 'peliculas.views.peliculas_por_lenguaje', name= "peliculas_por_lenguaje"),
    url(r'^form_mejor_puntuada/$', 'peliculas.views.form_mejor_puntuada', name= "form_mejor_puntuada"),
    url(r'^form_director/$', 'peliculas.views.form_director', name= "form_director")
)
