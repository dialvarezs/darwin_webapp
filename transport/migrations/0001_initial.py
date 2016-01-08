# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('company', models.CharField(max_length=32, verbose_name='empresa')),
                ('plate', models.CharField(blank=True, max_length=6, verbose_name='patente')),
                ('brand', models.CharField(max_length=32, verbose_name='marca')),
                ('model', models.CharField(max_length=32, verbose_name='modelo')),
                ('year', models.IntegerField(blank=True, verbose_name='año')),
                ('capacity', models.IntegerField(verbose_name='capacidad')),
                ('is_available', models.BooleanField(default=True, verbose_name='disponible')),
                ('notes', models.CharField(blank=True, max_length=128, verbose_name='notas')),
            ],
            options={
                'verbose_name': 'bus',
                'verbose_name_plural': 'buses',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=64, verbose_name='nombre')),
                ('short_name', models.CharField(max_length=8, verbose_name='nombre corto')),
                ('id_string', models.CharField(blank=True, max_length=16, verbose_name='RUT')),
                ('line_of_business', models.CharField(max_length=64, verbose_name='giro')),
                ('address', models.CharField(max_length=64, verbose_name='dirección')),
                ('email', models.EmailField(max_length=254, verbose_name='e-mail')),
            ],
            options={
                'verbose_name': 'empresa',
                'verbose_name_plural': 'empresas',
            },
        ),
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=32, verbose_name='nombre')),
                ('short_name', models.CharField(max_length=16, verbose_name='nombre corto')),
            ],
            options={
                'verbose_name': 'destino',
                'verbose_name_plural': 'destinos',
            },
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('id_string', models.CharField(max_length=16, verbose_name='RUT')),
                ('names', models.CharField(max_length=32, verbose_name='nombres')),
                ('surnames', models.CharField(max_length=32, verbose_name='apellidos')),
            ],
            options={
                'verbose_name': 'conductor',
                'verbose_name_plural': 'conductores',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('id_string', models.CharField(max_length=16, verbose_name='ID')),
                ('external_id', models.CharField(max_length=16, verbose_name='ID Externo')),
                ('debt', models.PositiveIntegerField(verbose_name='deuda')),
                ('charge', models.PositiveIntegerField(verbose_name='costo')),
                ('company', models.ForeignKey(verbose_name='empresa', to='transport.Company')),
            ],
            options={
                'verbose_name': 'grupo',
                'verbose_name_plural': 'grupos',
            },
        ),
        migrations.CreateModel(
            name='IDType',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=16, verbose_name='nombre')),
            ],
            options={
                'verbose_name': 'tipo de identificación',
                'verbose_name_plural': 'tipos de identificación',
            },
        ),
        migrations.CreateModel(
            name='Itinerary',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('app_people', models.IntegerField(verbose_name='PAX')),
                ('guides', models.IntegerField(verbose_name='guías')),
            ],
            options={
                'verbose_name': 'itinerario',
                'verbose_name_plural': 'itinerarios',
            },
        ),
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('id_string', models.CharField(max_length=16, verbose_name='identificación')),
                ('names', models.CharField(max_length=32, verbose_name='nombres')),
                ('surnames', models.CharField(max_length=32, verbose_name='apellidos')),
                ('date_of_birth', models.DateField(verbose_name='fecha de nacimiento')),
                ('sex', models.CharField(max_length=1, choices=[('m', 'masculino'), ('f', 'femenino')], verbose_name='sexo')),
                ('id_type', models.ForeignKey(verbose_name='tipo de identificación', to='transport.IDType')),
            ],
            options={
                'verbose_name': 'pasajero',
                'verbose_name_plural': 'pasajeros',
            },
        ),
        migrations.CreateModel(
            name='Stretch',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('description', models.CharField(max_length=64, verbose_name='descripción')),
            ],
            options={
                'verbose_name': 'tramo',
                'verbose_name_plural': 'tramos',
            },
        ),
        migrations.CreateModel(
            name='StretchDestinations',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('position', models.PositiveSmallIntegerField(verbose_name='posición')),
                ('destination', models.ForeignKey(verbose_name='destino', to='transport.Destination')),
                ('stretch', models.ForeignKey(to='transport.Stretch')),
            ],
            options={
                'verbose_name': 'destino',
                'verbose_name_plural': 'destinos',
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='Travel',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('date', models.DateField(verbose_name='fecha')),
                ('time', models.TimeField(null=True, blank=True, verbose_name='hora')),
                ('notes', models.CharField(blank=True, max_length=128, verbose_name='notas')),
                ('bus', models.ForeignKey(null=True, verbose_name='bus', blank=True, to='transport.Bus')),
                ('driver', models.ForeignKey(null=True, verbose_name='conductor', blank=True, to='transport.Driver')),
                ('group', models.ForeignKey(verbose_name='grupo', to='transport.Group')),
                ('itinerary', models.ForeignKey(verbose_name='itinerario', to='transport.Itinerary')),
            ],
            options={
                'verbose_name': 'viaje',
                'verbose_name_plural': 'viajes',
            },
        ),
        migrations.AddField(
            model_name='stretch',
            name='destinations',
            field=models.ManyToManyField(through='transport.StretchDestinations', to='transport.Destination'),
        ),
        migrations.AddField(
            model_name='itinerary',
            name='stretch',
            field=models.ForeignKey(verbose_name='tramo', to='transport.Stretch'),
        ),
        migrations.AddField(
            model_name='group',
            name='passengers',
            field=models.ManyToManyField(blank=True, to='transport.Passenger', verbose_name='pasajeros'),
        ),
        migrations.AddField(
            model_name='destination',
            name='stretchs',
            field=models.ManyToManyField(through='transport.StretchDestinations', to='transport.Stretch'),
        ),
    ]
