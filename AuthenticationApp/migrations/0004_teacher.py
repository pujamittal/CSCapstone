# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-28 02:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UniversitiesApp', '0005_auto_20161126_2116'),
        ('AuthenticationApp', '0003_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='university', to='UniversitiesApp.University')),
            ],
        ),
    ]
