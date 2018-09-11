from django import forms 
from .models import Caso, PerfilUsuario
from django.contrib.auth.models import User


class CasoForm(forms.ModelForm):

	class Meta:
		model = Caso
		fields = ('id', 'nombres', 'apellidos', 'cedula', 'departamento', 'descripcion', 'casotipo',)

	def __init__(self, *args, **kwargs):
         super(CasoForm, self).__init__(*args, **kwargs)
         for field in self.fields:
            	self.fields[field].widget.attrs.update({'class': 'form-control'})
         self.fields['descripcion'].widget.attrs.update({'class': 'form-control', 'rows' : '12'})
         self.fields['departamento'].widget.attrs.update({'class': 'form-control', 'onchange' : 'cargarSelect2(this.value);'})

class UserForm(forms.ModelForm):

	class Meta:

		model = User
		fields = ('first_name', 'last_name', 'email', 'username', 'password')

	def __init__(self, *args, **kwargs):
         super(UserForm, self).__init__(*args, **kwargs)
         for field in self.fields:
            	self.fields[field].widget.attrs.update({'class': 'form-control'})
         self.fields['username'].widget.attrs.update({'class': 'form-control', 'readonly' : ''})
         self.fields['password'].widget.attrs.update({'class': 'form-control', 'readonly' : ''})

class PerfilForm(forms.ModelForm):

	class Meta:

		model = PerfilUsuario
		fields = ('foto',)