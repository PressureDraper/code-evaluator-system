"""devtest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from devtest.views import *

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('login/', login),
    path('logout/', logout),
    path('docente/', maestros),
    path('alumno/', alumnos),
    path('alumnos/', mostrar_alumnos, name = "checkboxes_form"),
    path('perfil/', mostrar_perfil),
    path('grupo/', mostrar_grupo, name = "showgroup"),
    path('actividades/', mostrar_actividades),
    path('crear/', crear_actividades),
    path('detalles/', ver_detalles),
    path('crear/analisis', analizar_parametros, name = "precheck"),
    path('upload/', uploadFile),
    path('registros/', registros),
    # path('form/', page1),
    # path('data/', page2),
]
