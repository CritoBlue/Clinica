from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('atencion/pedirhora', views.pedir_hora, name='pedir_hora'),
    path('atencion/mishoras', views.mis_horas, name='mis_horas'),
    path('atencion/delete/<int:pk>', views.delete_hora, name='delete_hora'),
    path('atencion/pendientes/<int:pk>', views.pacientes_espera, name='pacientes_espera'),
    path('atencion/pendientes/terminar/<int:pk>', views.finish_hora, name='finish_hora'),

    path('recaudaciones/<int:sucursal_id>', views.recaudaciones, name='recaudaciones'),
    path('recaudaciones/generar_comisiones', views.generar_comisiones, name='generar_comisiones'),
    path('recaudaciones/generar_recaudaciones', views.generar_recaudaciones, name='generar_recaudaciones'),

    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),

    path('paciente/registro', views.paciente_registro, name='paciente_registro'),
    path('paciente/boletas', views.mis_boletas, name='mis_boletas'),

    path('medico/registro', views.medico_registro, name='medico_registro'),
    path('medico/miscomprobantes', views.mis_comprobantes, name='mis_comprobantes'),
]