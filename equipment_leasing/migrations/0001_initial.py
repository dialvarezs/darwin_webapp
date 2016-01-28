# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('id_string', models.CharField(max_length=16, verbose_name='identificación')),
                ('names', models.CharField(max_length=32, verbose_name='nombres')),
                ('surnames', models.CharField(max_length=32, verbose_name='apellidos')),
                ('sex', models.CharField(max_length=1, verbose_name='sexo', choices=[('m', 'masculino'), ('f', 'femenino')])),
                ('date_of_birth', models.DateField(verbose_name='fecha de nacimiento')),
                ('nationality', models.CharField(max_length=16, verbose_name='nacionalidad')),
            ],
            options={
                'verbose_name_plural': 'clientes',
                'verbose_name': 'cliente',
            },
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=16, verbose_name='nombre')),
                ('description', models.CharField(max_length=64, verbose_name='descipción')),
                ('price', models.PositiveIntegerField(verbose_name='precio')),
                ('quantity', models.PositiveIntegerField(verbose_name='cantidad')),
                ('stock', models.PositiveIntegerField(verbose_name='disponibles')),
            ],
        ),
        migrations.CreateModel(
            name='IDType',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=16, verbose_name='nombre')),
            ],
            options={
                'verbose_name_plural': 'tipos de identificación',
                'verbose_name': 'tipo de identificación',
            },
        ),
        migrations.CreateModel(
            name='Lease',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('client', models.ForeignKey(verbose_name='cliente', to='equipment_leasing.Client')),
            ],
        ),
        migrations.AddField(
            model_name='client',
            name='id_type',
            field=models.ForeignKey(verbose_name='tipo de identificación', to='equipment_leasing.IDType'),
        ),
    ]
