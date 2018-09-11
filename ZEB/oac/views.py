# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib import auth
from django.conf import settings
from .models import *
from .forms import *
from datetime import *
import json
import os
import sys


# Create your views here.

def Principal(request):

	return render(request, 'index.html',{},)

@permission_required('oac.add_caso', login_url="error_500")
def ConsultarCaso(request, ncaso):

	if ncaso != '':
		cason = ncaso
		
		try:

			consulta = Caso.objects.get(nrocaso=cason)
			if consulta.estado == 'Atendido':
				consulta2 =ReCaso.objects.get(caso_id=consulta.id)
				user = "%s %s"%(consulta2.user.first_name,consulta2.user.last_name)
				mensaje = consulta2.respuesta
			else:
				mensaje = ''
				user = ''

			formato = "%d/%m/%Y"
			fecha = consulta.creado
			return HttpResponse(
				json.dumps({'caso':consulta.nrocaso, 'cedula': consulta.cedula, 'estado': consulta.estado, 'personal': consulta.usuario.first_name, 'fecha': fecha.strftime(formato), 'respuesta': mensaje, 'personal': user }, ), content_type="application/json; charset=uft8")

		except ObjectDoesNotExist:

			mensaje = "error"
			return HttpResponse(
				json.dumps({'caso': mensaje}, ), content_type="application/json; charset=uft8")


@login_required
def Inicio(request):

	inicial = Caso.objects.all().count()
	casos = Caso.objects.filter(activo=True).order_by('-creado')
	usuarios = User.objects.filter(is_staff=0).filter(is_active=1).order_by('-date_joined')
	conteo_casos = Caso.objects.filter(activo=True).count()
	casos_respondidos = ReCaso.objects.filter(caso_id__activo=True).count()
	casos_user = Caso.objects.filter(usuario_id=request.user).filter(activo=True).count()
	casos_user_del = Caso.objects.filter(usuario_id=request.user).filter(activo=False).count()
	prom_aten = int((casos_user*100)/inicial)

	return render(request, 'index2.html',{'casos':casos, 'cantidad':conteo_casos, 'respuestas':casos_respondidos, 'personal':usuarios, 'user_aten':casos_user, 'user_eli': casos_user_del, 'promedio': prom_aten },)

# @permission_required('polls.can_vote', login_url="/login/")
@login_required
def ListaCasos(request):

	casos = Caso.objects.filter(activo=True).order_by('-creado')
	return render(request, 'pages/casos/lista_casos.html',{ 'casos': casos})

@permission_required('oac.add_caso', login_url="error_500")
def ListaCasosUsuario(request):

	casos = Caso.objects.filter(activo=True).order_by('-creado')
	return render(request, 'pages/casos/lista_casos_por_usuario.html',{ 'casos': casos, 'activo': 1})

@permission_required('oac.delete_caso', login_url="error_500")
def ListaCasosInactivos(request):

	casos = Caso.objects.filter(activo=False).order_by('-creado')
	return render(request, 'pages/casos/lista_casos_por_usuario.html',{ 'casos': casos})

def CasoEtiqueta(request, id):

	tag = Caso.objects.get(pk=id)
	return render(request, 'pages/casos/etiqueta_print.html',{'caso':tag},)	

@permission_required('oac.add_caso', login_url="error_500")
def AtencionCasos(request):

	if request.method == "POST":
		form = CasoForm(request.POST)
		if form.is_valid():
			nombres = request.POST['nombres']
			apellidos = request.POST['apellidos']
			cedula = request.POST['cedula']
			codigo = str('OAC-%s%s%s' % (nombres[0].upper(), apellidos[0].upper(), cedula[0:3]))
			caso = form.save(commit=False)
			caso.nrocaso = codigo
			caso.casotipo = request.POST['tipo']
			caso.usuario_id = request.user.id
			caso.save()
			return redirect('ListaCasos')
	else:
		form = CasoForm()
	return render(request, 'pages/casos/crear_caso.html', {'form' : form})

@permission_required('oac.change_caso', login_url="error_500")
def EditarCasos(request, pk):

	caso = get_object_or_404(Caso, pk=pk)
	if request.method == "POST":
		form = CasoForm(request.POST, instance=caso)
		if form.is_valid():
			nombres = request.POST['nombres']
			apellidos = request.POST['apellidos']
			cedula = request.POST['cedula']
			codigo = str('OAC-%s%s%s' % (nombres[0].upper(), apellidos[0].upper(), cedula[0:3]))
			caso = form.save(commit=False)
			caso.nrocaso = codigo
			caso.casotipo = request.POST['tipo']
			caso.save()
			return redirect('../../')
	else:
		form = CasoForm(instance=caso)
	return render(request,'pages/casos/crear_caso.html',{'form' : form, 'tipo': caso.casotipo})

@permission_required('oac.delete_caso', login_url="error_500")
def EliminarCaso(request):

	try:
		if request.POST['pk']:
			idcaso = request.POST['pk']
			caso = Caso.objects.filter(pk=idcaso).update(activo=False)
			
		return redirect('ListaCasos')

	except Exception, e:
		raise e


@permission_required('oac.change_recaso', login_url="error_500")
def ListaCasosAtendidos(request):

	casos = Caso.objects.filter(activo=True).order_by('-creado')
	return render(request, 'pages/casos/lista_casos_por_respuesta.html',{ 'casos': casos})

@login_required
def ContenidoCasos(request, id):

	caso = Caso.objects.get(pk=id)
	return render(request,'pages/casos/responder_caso.html',{'caso' : caso})

@login_required
def ContenidoRespuestaCaso(request, id):

	contenido = ReCaso.objects.get(caso_id=id)
	return HttpResponse(
		json.dumps({'respuesta': contenido.respuesta }), content_type="application/json; charset=uft8"
		)

@permission_required('oac.add_recaso', login_url="error_500")
def ResponderCaso(request, id):

	try:
		if request.POST['texto']:
			respuesta = ReCaso(respuesta=request.POST['texto'], caso_id=id, user_id=request.POST['user'])
			respuesta.save()
			estadocaso = Caso.objects.filter(pk=id).update(estado='Atendido')
			
		return redirect('ListaCasos')

	except Exception, e:
		raise e

@permission_required('oac.change_recaso', login_url="error_500")
def EditarRespCaso(request, id):

	try:
		if request.POST['texto']:
			respuesta = ReCaso.objects.filter(caso_id=id).update(respuesta=request.POST['texto'])
			
		return redirect('ListaCasos')

	except Exception, e:
		raise e


@login_required
def Error500(request):

	return render(request, 'pages/estados/500.html',{},)

@login_required
def ActualizarPerfil(request,id):

	usuario = request.user
   	perfil_usuario = usuario.perfilusuario
	if request.method == "POST":
		form = PerfilForm(request.POST, request.FILES, instance=perfil_usuario)
		formusuario = UserForm(request.POST, instance=usuario)
		if  formusuario.is_valid() and form.is_valid():
			foto = form.save(commit=False)
			datos = formusuario.save(commit=False)
			datos.save()
			foto.save()
			return redirect('Inicio')
	else:
		form = PerfilForm(instance=perfil_usuario)
		formusuario = UserForm(instance=request.user)
	return render(request,'pages/casos/perfil_usuario.html',{'form2': form, 'form': formusuario})

@permission_required('oac.add_caso', login_url="error_500")
def RequisitosCaso(request, dep):

	try:
		requisito = TipoCaso.objects.get(caso=dep)
		return HttpResponse(json.dumps({'requisitos': requisito.descripcion, 'caso': requisito.caso, 'departamento': requisito.departamento, 'preguntas': requisito.preguntasf }), content_type="application/json; charset=uft8")
	except Exception, e:
		raise e
	

from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter


def ExportarPDF(request):


	response = HttpResponse(content_type='application/pdf')
	pdf_name = "clientes.pdf"  # llamado clientes
	# la linea 26 es por si deseas descargar el pdf a tu computadora

	response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
	buff = BytesIO()
	doc = SimpleDocTemplate(buff,
	                        pagesize=letter,
	                        rightMargin=40,
	                        leftMargin=40,
	                        topMargin=60,
	                        bottomMargin=18,
	                        )
	clientes = []
	styles = getSampleStyleSheet()
	header = Paragraph("Listado de Clientes", styles['Heading1'])
	clientes.append(header)
	headings = ('Nombres', 'Apellidos', 'Cedula', 'Departamento',)
	allclientes = [(p.nombres, p.apellidos, p.cedula, p.departamento) for p in Caso.objects.all()]
	print allclientes

	t = Table([headings] + allclientes)
	t.setStyle(TableStyle(
	    [
	        ('GRID', (0, 0), (3, -1), 1, colors.dodgerblue),
	        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
	        ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
	    ]
	))
	clientes.append(t)
	doc.build(clientes)
	response.write(buff.getvalue())
	buff.close()
	return response

from reportlab.pdfgen import canvas 
from reportlab.lib.pagesizes import A4, cm 
from reportlab.lib.enums import TA_CENTER
import time

@permission_required('oac.add_caso', login_url="error_500")
def CanvasPDF(request):

	response = HttpResponse(content_type='application/pdf')
	fecha = ''
	fecha = request.POST['fecha']
	buscarf = ('%s-%s-%s') %(fecha[6:10],fecha[0:2],fecha[3:5])
	print buscarf
	pdf_name = "clientes.pdf"  # llamado clientes
	# la linea 26 es por si deseas descargar el pdf a tu computadora
	response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
	buff = BytesIO()
	c = canvas.Canvas(buff, pagesize=letter)

	#Cabecera
	c.setLineWidth(.3)
	c.setFont('Helvetica-Bold', 18)
	c.drawString(60,650,'Reporte de Casos Atendidos en la Oficina de Atención al')
	c.drawString(150,630,'Ciudadano de la Zona Educativa Barinas')

	c.setFont('Helvetica-Bold',14)
	c.drawString(420,700,"Fecha: %s" %time.strftime('%d/%m/%Y'))
	c.line(417,697,539,697)

	#Logos
	logohead = 'media/logos/logo-mppe.jpg'
	logofooter = 'media/logos/cintillo_footer.png'
	c.drawImage(logohead, 30, 720, width=110, height=50)
	c.drawImage(logofooter, 20, 40, width=580, height=50)

	#Pie de pagina
	c.setLineWidth(1)
	c.setFont('Helvetica-Bold', 14)
	c.line(250,150,400,150)
	c.drawString(260,120,'Lcda. Yennis Perez')
	c.drawString(230,105,'Coordinadora de OAC Barinas')

	#Cabecera de la tabla
	styles = getSampleStyleSheet()
	styleBH = styles["Normal"]
	styleBH.alignment = TA_CENTER
	styleBH.fontSize = 10
	styleBH.fontName = 'Helvetica-Bold'

	numero = Paragraph('''N° caso''',styleBH)
	nombre = Paragraph('''Nombres y Apellidos''',styleBH)
	cedula = Paragraph('''Cedula''', styleBH)
	departamento = Paragraph('''Departamento''', styleBH)
	creado = Paragraph('''Fecha de Atencion''', styleBH)
	usuario = Paragraph('''Atendido por''', styleBH)

	data= []

	data.append([numero, cedula,nombre,departamento,creado,usuario])

	#Tabla
	styleN = styles["BodyText"]
	styleN.alignment = TA_CENTER
	styleN.fontSize = 7


	high = 580
	centrar = 0
	izquierda = 0

	conteo = Caso.objects.all().count()
	casos = Caso.objects.filter(activo=True).filter(creado=buscarf).order_by('creado').order_by('departamento').order_by('cedula')

	for caso in casos: 
		nombre = caso.nombres
		apellido =  ' ' + caso.apellidos
		fullname = nombre + apellido
		allcasos = [caso.nrocaso, caso.cedula, fullname.upper(), caso.departamento, caso.creado.strftime("%d-%m-%Y"), caso.usuario]
		data.append(allcasos)
		high = high - 18
		centrar = centrar + 1
		izquierda = izquierda + 1

	#Tama#o de tabla
	width, height = A4
	table = Table(data, colWidths=[2.3 * cm, 3 * cm, 5 * cm, 3 * cm, 3 * cm, 3 * cm ])
	table.setStyle(TableStyle([
	        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
	        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
	        ('LINEABOVE', (0, 0), (5, 1), 1, colors.black),
	        ('LINEBEFORE', (0, 0), (6, 0), 1, colors.black),
	        ('BACKGROUND', (0, 0), (6, 0), colors.lightgrey),
	        ('ALIGN',(0, 0),(5, centrar),'CENTER'),
	        ('ALIGN',(2, 0),(2, izquierda),'LEFT'),

	    ]))

	#PDF size
	table.wrapOn(c, width, height)
	table.drawOn(c, 30, high)
	c.showPage()


	c.save()

	pdf = buff.getvalue()
	buff.close()
	response.write(pdf)
	return response

@permission_required('oac.add_caso', login_url="error_500")
def ReporteCasos(request):

	atendidos = Caso.objects.filter(activo=True).count()
	respondidos = ReCaso.objects.filter(caso_id__activo=True).count()
	registrados = atendidos-respondidos
	barra = int((respondidos*100)/atendidos)
	barra2 = int((registrados*100)/atendidos)
	return render(request, 'pages/casos/reporte_casos.html',{'casos': atendidos, 'respuestas': respondidos, 'total':barra, 'total1':barra2, 'esperando':registrados},)