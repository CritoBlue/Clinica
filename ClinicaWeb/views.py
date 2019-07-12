#Django stuff
from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime
#User and login/logout
#from django.conf import settings
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import user_passes_test, login_required
#App forms and models
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView
from .models import Medico, Paciente, HoraAtencion, InformeRecaudacion, Sucursal, Boleta, Comision, Especialidad
from .forms import PacienteForm, MedicoForm, LoginForm, AtencionForm

#User = settings.AUTH_USER_MODEL

def index(request):
	sucursales = Sucursal.objects.all()

	context = { 'sucursales' : sucursales }

	return render(request, 'index.html', context)

@login_required(login_url='login')
def pedir_hora(request):
	atentionform = AtencionForm()
	sucursales = Sucursal.objects.all()

	if request.method == 'POST':
		atentionform = AtencionForm(request.POST)
		if atentionform.is_valid():
			atentionform.save(commit=False)
			this_fechaAtencion = atentionform.cleaned_data['fechaAtencion']
			this_horaAtencion = atentionform.cleaned_data['horaAtencion']
			this_sucursal = atentionform.cleaned_data['sucursal']
			this_especialidad = atentionform.cleaned_data['especialidad']
			this_valor = this_especialidad.valor
			atentionform.instance.valor = this_valor
			this_medico = atentionform.cleaned_data['medico']
			this_paciente = Paciente.objects.all()
			this_paciente = this_paciente.get(user=request.user)
			atentionform.instance.paciente = this_paciente

			atentionform.save()
			return redirect('mis_horas')
		else:
			print(atentionform.errors)
	else:
		atentionform = AtencionForm()

	context = { 
		'form' : atentionform,
		'sucursales' : sucursales
	}

	return render(request, 'pedir_hora.html', context)

@login_required(login_url='login')
def mis_horas(request):
	sucursales = Sucursal.objects.all()
	qs_hora = HoraAtencion.objects.all()
	qs_hora = qs_hora.filter(paciente=request.user.paciente)
	qs_hora = qs_hora.filter(estado=0)

	context = { 
		"horas" : qs_hora,
		'sucursales' : sucursales
	}

	return render(request, "mis_horas.html", context)

def delete_hora(request, pk):
	HoraAtencion.objects.filter(id=pk).delete()
	return redirect('mis_horas')

@login_required(login_url='login')
def mis_boletas(request):
	sucursales = Sucursal.objects.all()
	qs_boleta = Boleta.objects.all()
	qs_boleta = qs_boleta.filter(horaAtencion__paciente=request.user.paciente)

	context = { 
		"boletas" : qs_boleta,
		'sucursales' : sucursales
	}

	return render(request, "mis_boletas.html", context)

@login_required(login_url='login')
def pacientes_espera (request, pk):
	sucursales = Sucursal.objects.all()
	user = User.objects.get(pk=pk)
	medico = Medico.objects.get(user=user)
	espera = HoraAtencion.objects.all()
	espera = espera.filter(medico=medico, estado=0)

	context = {
		"sucursales" : sucursales,
		"espera" : espera
	}

	return render(request, "pacientes_espera.html", context)

@login_required(login_url='login')
def finish_hora(request, pk):
	#Cambiar estado de Hora Médica
	hora = HoraAtencion.objects.get(pk=pk)
	hora.estado = 1
	hora.save()

	#Generar Boleta
	valorTotal = round(hora.valor * 1.19)

	boleta = Boleta(
		valorTotal = valorTotal,
		horaAtencion = HoraAtencion.objects.get(pk=pk)
	)

	boleta.save()

	return redirect('pacientes_espera', pk=request.user.pk)

def mis_comprobantes(request):
	sucursales = Sucursal.objects.all()
	
	medico = request.user.medico
	qs_comprobante = Comision.objects.filter(medico=medico).order_by('-pk')

	context = { 
		"sucursales" : sucursales,
		"comprobantes" : qs_comprobante
	}

	return render(request, "comprobante_pago.html", context)

def generar_comisiones(request):
	mes = datetime.datetime.now().month
	año = datetime.datetime.now().year
	qs_medico = Medico.objects.all()

	for medico in qs_medico:
		sucursal = medico.sucursal
		especialidad = medico.especialidad
		horasAtencion = HoraAtencion.objects.filter(medico=medico)
		totalComision = 0

		for horas in horasAtencion:
			boleta = Boleta.objects.get(horaAtencion=horas)
			totalComision = totalComision + round(boleta.valorTotal * 0.2)

		comision, created = Comision.objects.update_or_create(
			mes = mes,
			año = año,
			medico = medico
		)

		comision.totalComision = totalComision
		comision.sucursal = sucursal
		comision.especialidad = especialidad
		comision.save()
	
	return redirect('index')

@login_required(login_url='login')
def recaudaciones(request, sucursal_id):
	sucursales = Sucursal.objects.all()
	this_sucursal = sucursales.get(id=sucursal_id)
	this_sucursal = this_sucursal.nombre
	qs_recauda = InformeRecaudacion.objects.all()
	qs_recauda = qs_recauda.filter(sucursal=sucursal_id)


	context = { 
		"recauda" : qs_recauda,
		"sucursales" : sucursales,
		"sucursal" : this_sucursal
	}
	return render(request, "recaudaciones.html", context)

def generar_recaudaciones(request):
	mes = datetime.datetime.now().month
	año = datetime.datetime.now().year
	qs_sucursales = Sucursal.objects.all()

	for sucursal in qs_sucursales:
		horasAtencion = HoraAtencion.objects.filter(sucursal=sucursal)
		totalRecaudado = 0
		
		for horas in horasAtencion:
			boleta = Boleta.objects.get(horaAtencion=horas)
			totalRecaudado = totalRecaudado + boleta.valorTotal

		recaudado, created = InformeRecaudacion.objects.update_or_create(
			mes = mes,
			año = año,
			sucursal = sucursal
		)

		recaudado.totalRecaudado = totalRecaudado
		recaudado.save()
	return redirect('index')

def paciente_registro(request):
	pacienteform = PacienteForm()
	sucursales = Sucursal.objects.all()

	if request.method == 'POST':
		pacienteform = PacienteForm(request.POST)
		if pacienteform.is_valid():
			pacienteform.save(commit=True)
			user = User.objects.latest('date_joined')
			rut = pacienteform.cleaned_data['rut']
			tel = pacienteform.cleaned_data['tel']
			prevision = pacienteform.cleaned_data['prevision']
			paciente = Paciente(
				user=user, 
				rut=rut, 
				tel=tel, 
				prevision=prevision
			)
			paciente.save()
			pacienteform = PacienteForm()
			return redirect('login')
		else:
			print(pacienteform.errors)
	else:
		pacienteform = PacienteForm()

	tipo = 'Paciente'

	context = { 
		"form" : pacienteform, 
		"tipo" : tipo ,
		"sucursales" : sucursales,
	}

	return render(request, "registro.html", context)

def medico_registro(request):
	medicoform = MedicoForm()
	sucursales = Sucursal.objects.all()

	if request.method == 'POST':
		medicoform = MedicoForm(request.POST)
		if medicoform.is_valid():
			medicoform.save(commit=True)
			user = User.objects.latest('date_joined')
			user.is_staff = True
			user.save()
			rut = medicoform.cleaned_data['rut']
			tel = medicoform.cleaned_data['tel']
			salary = medicoform.cleaned_data['salario']
			especialidad = medicoform.cleaned_data['especialidad']
			sucursal = medicoform.cleaned_data['sucursal']
			medico = Medico(
				user=user, 
				rut=rut, 
				tel=tel, 
				salario=salary, 
				especialidad=especialidad, 
				sucursal=sucursal
			)
			medico.save()
			medicoform = MedicoForm()
			return redirect('index')
		else:
			print(medicoform.errors)

	tipo = 'Medico'

	context = { 
		"form" : medicoform, 
		"tipo" : tipo,
		"sucursales" : sucursales
	}

	return render(request, "registro.html", context)

def login_view(request):
	next = request.GET.get('next')
	sucursales = Sucursal.objects.all()
	form = LoginForm(request.POST or None)
	
	context = { 
		"form" : form,
		"sucursales" : sucursales
	}

	if form.is_valid():
		username = form.cleaned_data.get('username')
		password = form.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		login(request, user)
		if next:
			return redirect(next)
		return redirect('index')

	return render(request, "login.html", context)

def logout_view(request):
	logout(request)
	return redirect('index')