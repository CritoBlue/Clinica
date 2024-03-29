# Generated by Django 2.2.2 on 2019-07-12 07:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comuna',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Especialidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Especialidades',
            },
        ),
        migrations.CreateModel(
            name='Prevision',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Previsiones',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': 'Regiones',
            },
        ),
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=100)),
                ('comuna', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ClinicaWeb.Comuna')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ClinicaWeb.Region')),
            ],
            options={
                'verbose_name_plural': 'Sucursales',
            },
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut', models.CharField(max_length=10, unique=True)),
                ('tel', models.CharField(max_length=9)),
                ('prevision', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ClinicaWeb.Prevision')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Medico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut', models.CharField(max_length=10, unique=True)),
                ('tel', models.CharField(max_length=9)),
                ('salario', models.IntegerField(default=400000)),
                ('especialidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ClinicaWeb.Especialidad')),
                ('sucursal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ClinicaWeb.Sucursal')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InformeRecaudacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mes', models.IntegerField(default=1)),
                ('año', models.PositiveIntegerField(default=2019)),
                ('fechaEmision', models.DateField(auto_now_add=True, verbose_name='Fecha de Emisión')),
                ('totalRecaudado', models.PositiveIntegerField(default=0)),
                ('sucursal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ClinicaWeb.Sucursal')),
            ],
            options={
                'verbose_name_plural': 'InformesRecaudacion',
            },
        ),
        migrations.CreateModel(
            name='HoraAtencion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaAtencion', models.DateField(verbose_name='Fecha de Atención')),
                ('horaAtencion', models.CharField(choices=[('07:00', '07:00'), ('07:30', '07:30'), ('08:00', '08:00'), ('08:30', '08:30'), ('09:00', '09:00'), ('09:30', '09:30'), ('10:00', '10:00'), ('10:30', '10:30'), ('11:00', '11:00'), ('11:30', '11:30'), ('12:00', '12:00'), ('12:30', '12:30'), ('13:00', '13:00'), ('13:30', '13:30'), ('14:00', '14:00'), ('14:30', '14:30'), ('15:00', '15:00'), ('15:30', '15:30'), ('16:00', '16:00'), ('16:30', '16:30'), ('17:00', '17:00'), ('17:30', '17:30'), ('18:00', '18:00'), ('18:30', '18:30'), ('19:00', '19:00'), ('19:30', '19:30'), ('20:00', '20:00'), ('20:30', '20:30'), ('21:00', '21:00'), ('21:30', '21:30'), ('22:00', '22:00')], default=0, max_length=5)),
                ('valor', models.IntegerField(default=3000)),
                ('estado', models.CharField(choices=[(0, 'Pendiente'), (1, 'Terminado')], default=0, max_length=1)),
                ('especialidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ClinicaWeb.Especialidad')),
                ('medico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ClinicaWeb.Medico')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ClinicaWeb.Paciente')),
                ('sucursal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ClinicaWeb.Sucursal')),
            ],
            options={
                'verbose_name_plural': 'HorasAtencion',
            },
        ),
        migrations.AddField(
            model_name='comuna',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ClinicaWeb.Region'),
        ),
        migrations.CreateModel(
            name='Comision',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mes', models.PositiveIntegerField(default=1)),
                ('año', models.PositiveIntegerField(default=2019)),
                ('fechaEmision', models.DateField(auto_now_add=True, verbose_name='Fecha de Emisión')),
                ('totalComision', models.PositiveIntegerField(default=0)),
                ('especialidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ClinicaWeb.Especialidad')),
                ('medico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ClinicaWeb.Medico')),
                ('sucursal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ClinicaWeb.Sucursal')),
            ],
            options={
                'verbose_name_plural': 'Comisiones',
            },
        ),
        migrations.CreateModel(
            name='Boleta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valorTotal', models.IntegerField(default=0)),
                ('fechaEmision', models.DateField(auto_now_add=True, verbose_name='Fecha de Emisión')),
                ('horaAtencion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ClinicaWeb.HoraAtencion')),
            ],
        ),
    ]
