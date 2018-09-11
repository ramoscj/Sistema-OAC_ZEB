"""ZEB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import include, url
from django.contrib.auth.views import login, logout
from django.core.urlresolvers import reverse_lazy
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [

    #urls principal
    url(r'^$', views.Principal, name='index'),
    url(r'^consultar_caso/(?P<ncaso>.*)/$', views.ConsultarCaso, name='consultar_caso'),
	url(r'^principal/$', views.Inicio, name='Inicio'),

    #urls de lista general de casos y crear nuevos casos
    url(r'^principal/casos/$', views.ListaCasos, name='ListaCasos'),
    url(r'^principal/casos/registro_caso/$', views.AtencionCasos, name='AtencionCasos'),
    url(r'^principal/casos/registro_caso/requisitos/(?P<dep>.*)/$', views.RequisitosCaso, name='requisitos_caso'),
    url(r'^principal/reportes/$', views.ReporteCasos, name='reporte_casos'),
    
    #urls de casos atendidos por usuario
    url(r'^principal/casos_usuario/$', views.ListaCasosUsuario, name='ListaCasosUsuario'),
    url(r'^principal/casos_inactivos/$', views.ListaCasosInactivos, name='ListaCasosInactivos'),
    url(r'^principal/casos_usuario/eliminar_caso/$', views.EliminarCaso, name='EliminarCaso'),
    url(r'^principal/casos_usuario/editar/(?P<pk>[0-9]+)/$', views.EditarCasos, name='EditarCasos'),
 
    #urls de casos atendidos por departamento
    url(r'^casos_respondidos/$', views.ListaCasosAtendidos, name='ListaCasosAtendidos'),
    url(r'^casos_respondidos/contenido/(?P<id>[0-9]+)/$', views.ContenidoCasos, name='ContenidoCasos'),
    url(r'^casos_respondidos/contenido/(?P<id>[0-9]+)/responder/$', views.ResponderCaso, name='ResponderCaso'),
    url(r'^casos_respondidos/contenido/(?P<id>[0-9]+)/respuesta_caso/$', views.ContenidoRespuestaCaso, name='ContenidoRespuestaCaso'),
    url(r'^casos_respondidos/contenido/(?P<id>[0-9]+)/editar_respuesta/$', views.EditarRespCaso, name='EditarRespCaso'),

    #urls pdf
    url(r'^principal/reportes/generar_pdf/$', views.CanvasPDF, name='generar_pdf'),
     #urls pdf
    url(r'^casos_respondidos/contenido/(?P<id>[0-9]+)/generar_etiqueta/$', views.CasoEtiqueta, name='caso_etiqueta'),

    #urls de sesiones
    url(r'^login/$', login, {'template_name': 'pages/sesiones/ingresar.html'}, name='misitio_ingresar'),
    url(r'^logout/$', logout, {'next_page': 'misitio_ingresar'}, name='misitio_salir'),

    #ursl para usuarios
    url(r'^perfil_usuario/(?P<id>[0-9]+)/$', views.ActualizarPerfil, name='perfil_usuario'),

    #urls para mostrar errores generales
    url(r'^error/$', views.Error500, name='error_500'),

    # url(r'^reporte_nuevo/$', views.AtencionCasos, name='AtencionCasos'),
    # url(r'^reporte_nuevo/(?P<pk>[0-9]+)/editar/$', views.EditarCasos, name='EditarCasos'),
    # url(r'^responder_caso/$', views.GuardarRespCaso, name='GuardarRespCaso'),
    # url(r'^cargar_respuesta_contenido/(?P<id>\d+)$', views.RespuestaCaso, name='RespuestaCaso'),
    # # url(r'^test/(?P<texto>\w+)/(?P<idcaso>\d+)$', views.SaveResp, name='SaveResp'),
    # # url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
    # url(r'^test/$', views.Test, name='Test'),
] 
if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
