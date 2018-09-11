# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-05 14:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('oac', '0012_auto_20170203_1758'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatosUsuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departamento', models.CharField(blank=True, choices=[('Despacho', 'Despacho'), ('Personal', 'Personal'), ('Juridica', 'Juridica'), ('Inicial', 'Inicial'), ('Especial', 'Especial'), ('Primaria', 'Primaria'), ('Media General', 'Media General'), ('Educ. para Adultos', 'Educ. para Adultos'), ('H.C.M', 'H.C.M')], max_length=140, null=True)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]