import datetime
from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Paciente, Medico, Prevision, Especialidad, Sucursal, HoraAtencion

User = get_user_model()

class UserForm(UserCreationForm):
 	class Meta(UserCreationForm):
 		model = User
 		fields = (
 			'username',
 			'email',
 			'first_name',
 			'last_name'
 		)

class PacienteForm(UserForm):
	rut = forms.CharField(label='RUT', required=True)
	tel = forms.CharField(label='Teléfono', required=True)
	prevision = forms.ModelChoiceField(label='Previsión', queryset=Prevision.objects.all(), empty_label="Seleccione...")

	def save(self, commit=True):
		paciente = super().save(commit=False)
		paciente.user = User.objects.latest('date_joined')

		if commit:
			paciente.save()
			return paciente

class MedicoForm(UserForm):
	rut = forms.CharField(label='RUT', required=True)
	tel = forms.CharField(label='Teléfono', required=True)
	salario = forms.IntegerField(label='Salario', required=True)
	especialidad = forms.ModelChoiceField(label='Especialidad', queryset=Especialidad.objects.all(), empty_label="Seleccione…")
	sucursal = forms.ModelChoiceField(label='Sucursal', queryset=Sucursal.objects.all(), empty_label="Seleccione…")

	def save(self, commit=True):
		medico = super().save(commit=False)
		medico.user = User.objects.latest('date_joined')
		if commit:
			medico.save()
			return medico

class LoginForm (forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True, widget=forms.PasswordInput)

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')

		if username and password:
			user = authenticate(username=username, password=password)
			if not user:
				raise forms.ValidationError("El usuario no existe")
			if not user.check_password(password):
				raise forms.ValidationError("Nombre de usuario o contraseña son incorrectos")
			if not user.is_active:
				raise forms.ValidationError("El usuario no está activo")
		return super(LoginForm, self).clean(*args, **kwargs)

class AtencionForm(forms.ModelForm):
	fechaAtencion = forms.DateField(label='Fecha de Atención', widget=forms.SelectDateWidget)

	class Meta:
		model = HoraAtencion
		fields = (
			'fechaAtencion',
			'horaAtencion',
			'sucursal',
			'especialidad',
			'medico'
		)