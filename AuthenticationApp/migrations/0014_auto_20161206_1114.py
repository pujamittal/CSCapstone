# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-06 16:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GroupsApp', '0002_group_project'),
        ('AuthenticationApp', '0013_auto_20161205_1423'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='groups',
            field=models.ManyToManyField(blank=True, null=True, to='GroupsApp.Group'),
        ),
        migrations.AlterField(
            model_name='student',
            name='university',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student_university', to='UniversitiesApp.University'),
        ),
    ]
