# Generated by Django 2.2.2 on 2019-07-12 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ClinicaWeb', '0002_auto_20190712_0347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='horaatencion',
            name='estado',
            field=models.IntegerField(choices=[(0, 'Pendiente'), (1, 'Terminado')], default=0),
        ),
    ]
