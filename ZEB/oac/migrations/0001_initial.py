# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-29 01:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Casos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=140)),
                ('apellidos', models.CharField(max_length=140)),
                ('cedula', models.IntegerField()),
                ('departamento', models.IntegerField(choices=[(1, 'Despacho'), (2, 'Personal'), (3, 'Juridica'), (4, 'Inicial'), (5, 'Especial'), (6, 'Primaria'), (7, 'Media General'), (8, 'Educ. para Adultos'), (9, 'H.C.M')])),
                ('caso', models.TextField()),
            ],
        ),
    ]