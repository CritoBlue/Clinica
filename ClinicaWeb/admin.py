from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Region, Comuna, Especialidad, Sucursal, Prevision, Medico, Paciente, HoraAtencion, Boleta, Comision, InformeRecaudacion

admin.site.register(Region)
admin.site.register(Comuna)
admin.site.register(Especialidad)
admin.site.register(Sucursal)
admin.site.register(Prevision)
admin.site.register(Medico)
admin.site.register(Paciente)
admin.site.register(HoraAtencion)
admin.site.register(Boleta)
admin.site.register(Comision)
admin.site.register(InformeRecaudacion)