# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-07 15:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ProjectsApp', '0007_project_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='created_by',
        ),
    ]