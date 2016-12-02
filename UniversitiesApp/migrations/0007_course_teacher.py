# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-02 01:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AuthenticationApp', '0006_engineer'),
        ('UniversitiesApp', '0006_merge_20161128_1926'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='AuthenticationApp.Teacher'),
        ),
    ]