# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0002_remove_bus_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusCompany',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=32, verbose_name='nombre')),
            ],
            options={
                'verbose_name_plural': 'empresas de buses',
                'verbose_name': 'empresa de buses',
            },
        ),
        migrations.AddField(
            model_name='bus',
            name='company',
            field=models.ForeignKey(default=1, to='transport.BusCompany', verbose_name='empresa'),
            preserve_default=False,
        ),
    ]
