from django.contrib.auth.models import User
#from django.conf import settings
from django.db import models
import datetime

class Region(models.Model):
	nombre = models.CharField(max_length=30)

	def __str__(self):
		return self.nombre
	class Meta:
		verbose_name_plural = 'Regiones'

class Comuna(models.Model):
	nombre = models.CharField(max_length=50)
	region = models.ForeignKey(Region, on_delete = models.CASCADE)

	def __str__(self):
		return self.nombre

class Especialidad(models.Model):
	nombre = models.CharField(max_length=100)
	valor = models.IntegerField(default=3000)

	def __str__(self):
		return self.nombre
	class Meta:
		verbose_name_plural = 'Especialidades'

class Sucursal(models.Model):
	nombre = models.CharField(max_length=100)
	direccion = models.CharField(max_length=100)
	comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
	region = models.ForeignKey(Region, on_delete=models.CASCADE)

	def __str__(self):
		return self.nombre
	class Meta:
		verbose_name_plural = 'Sucursales'

class Prevision(models.Model):
	nombre = models.CharField(max_length=100)

	def __str__(self):
		return self.nombre
	class Meta:
		verbose_name_plural = 'Previsiones'

class Medico(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	rut = models.CharField(max_length=10, unique=True)
	tel = models.CharField(max_length=9)
	salario = models.IntegerField(default=400000)
	especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)
	sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)

	def __str__(self):
		return self.user.first_name + ' ' + self.user.last_name

class Paciente(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	rut = models.CharField(max_length=10, unique=True)
	tel = models.CharField(max_length=9)
	prevision = models.ForeignKey(Prevision, on_delete=models.CASCADE)

	def __str__(self):
		return self.user.first_name + ' ' + self.user.last_name

class HoraAtencion(models.Model):
	STATUS_CHOICES = (
		(0, "Pendiente"),
		(1, "Terminado")
	)

	TIME_CHOICES = (
		('09:00', '09:00'),
		('09:30', '09:30'),
		('10:00', '10:00'),
		('10:30', '10:30'),
		('11:00', '11:00'),
		('11:30', '11:30'),
		('12:00', '12:00'),
		('12:30', '12:30'),
		('13:00', '13:00'),
		('13:30', '13:30'),
		('14:00', '14:00'),
		('14:30', '14:30'),
		('15:00', '15:00'),
		('15:30', '15:30'),
		('16:00', '16:00'),
		('16:30', '16:30'),
		('17:00', '17:00'),
		('17:30', '17:30'),
		('18:00', '18:00'),
		('18:30', '18:30'),
		('19:00', '19:00'),
		('19:30', '19:30'),
		('20:00', '20:00')
	)

	fechaAtencion = models.DateField('Fecha de Atención')
	horaAtencion = models.CharField(max_length=5, choices=TIME_CHOICES, default='09:00')
	valor = models.IntegerField(default=3000)
	estado = models.IntegerField(choices=STATUS_CHOICES, default=0)
	sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
	especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)
	medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
	paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)

	def __str__(self):
		return self.paciente.user.first_name + ' ' + str(self.fechaAtencion.year) + str(self.fechaAtencion.month) + str(self.fechaAtencion.day) + str(self.horaAtencion)
	class Meta:
		verbose_name_plural = 'HorasAtencion'

class Boleta(models.Model):
	valorTotal = models.IntegerField(default=0) 
	emision = models.DateTimeField('Fecha de Emisión', auto_now_add=True)
	horaAtencion = models.OneToOneField(HoraAtencion, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.id)

class Comision(models.Model):
	mes = models.PositiveIntegerField(default=1)
	año = models.PositiveIntegerField(default=2019)
	fechaEmision = models.DateField('Fecha de Emisión', auto_now_add=True)
	totalComision = models.PositiveIntegerField(default=0)
	medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
	sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
	especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)

	def __str__(self):
		return self.medico.user.first_name + ' ' + str(self.año) + ' ' + str(self.mes)
	class Meta:
		verbose_name_plural = 'Comisiones'

class InformeRecaudacion(models.Model):
	mes = models.IntegerField(default=1)
	año = models.PositiveIntegerField(default=2019)
	fechaEmision = models.DateField('Fecha de Emisión', auto_now_add=True)
	totalRecaudado = models.PositiveIntegerField(default=0)
	sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)

	def __str__(self):
		return self.sucursal.nombre + ' ' + str(self.año) + ' ' + str(self.mes)
	class Meta:
		verbose_name_plural = 'InformesRecaudacion'