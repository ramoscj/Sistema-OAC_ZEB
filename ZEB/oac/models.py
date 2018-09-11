from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Caso(models.Model):
	departamentos = (
			('Despacho','Despacho'),
			('Personal','Personal'),
			('Juridica','Juridica'),
			('Eponimo','Eponimo'),
			('Pago Directo','Pago Directo'),
			('Jubilacion','Jubilacion'),
			('Comunidades Educativas','Comunidades Educativas'),
			('Notas','Notas'),
			('Inicial','Inicial'),
			('Especial','Especial'),
			('Primaria','Primaria'),
			('Media General','Media General'),
			('Educ. para Adultos','Educ. para Adultos'),
			('H.C.M','H.C.M'),

		)
	estados = (
			('Por atender','Por atender'),
			('Atendido','Atendido'),
			('Respondiendo','Respondiendo')

		)

	def __unicode__(self):
		return self.nombres

	def codigo_caso(self):
		ced = str(self.cedula)
		codigo = str('OAC-%s%s%s' % (self.nombres[0].upper(), self.apellidos[0].upper(), ced[0:3]))
		return codigo

	nombres = models.CharField(max_length=140)
	apellidos = models.CharField(max_length=140)
	cedula = models.IntegerField()
	departamento =  models.CharField(max_length=100, choices=departamentos)
	descripcion = models.TextField()
	creado = models.DateField(auto_now=True)
	estado = models.CharField(max_length=50, choices=estados, default='Por atender', null=True)
	activo = models.BooleanField(default=True)
	casotipo = models.CharField(max_length=140, blank=True)
	nrocaso = models.CharField(max_length=140, blank=True)
	usuario = models.ForeignKey(User)

	

class ReCaso(models.Model):
	respuesta = models.TextField()
	caso = models.OneToOneField(Caso, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __unicode__(self):
		return self.respuesta

class PerfilUsuario(models.Model):

	departamentos = (
			('Despacho','Despacho'),
			('Personal','Personal'),
			('Juridica','Juridica'),
			('Eponimo','Eponimo'),
			('Pago Directo','Pago Directo'),
			('Jubilacion','Jubilacion'),
			('Comunidades Educativas','Comunidades Educativas'),
			('Notas','Notas'),
			('Inicial','Inicial'),
			('Especial','Especial'),
			('Primaria','Primaria'),
			('Media General','Media General'),
			('Educ. para Adultos','Educ. para Adultos'),
			('H.C.M','H.C.M'),
			('Atencion OAC','Atencion OAC'),

		)

	departamento = models.CharField(max_length=140, choices=departamentos, blank=True, null=True)
	foto = models.ImageField(upload_to='avatars',null=True,blank=True)
	usuario = models.OneToOneField(User, on_delete=models.CASCADE)

class TipoCaso(models.Model):

	departamentos = (
			('Despacho','Despacho'),
			('Personal','Personal'),
			('Juridica','Juridica'),
			('Eponimo','Eponimo'),
			('Pago Directo','Pago Directo'),
			('Jubilacion','Jubilacion'),
			('Comunidades Educativas','Comunidades Educativas'),
			('Notas','Notas'),
			('Inicial','Inicial'),
			('Especial','Especial'),
			('Primaria','Primaria'),
			('Media General','Media General'),
			('Educ. para Adultos','Educ. para Adultos'),
			('H.C.M','H.C.M'),

		)

	departamento = models.CharField(max_length=140, choices=departamentos, blank=True, null=True)
	caso = models.CharField(max_length=140)
	descripcion = models.TextField()
	preguntasf = models.TextField(blank=True)