# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-05 03:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UniversitiesApp', '0007_course_teacher'),
        ('AuthenticationApp', '0008_auto_20161202_1039'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='university',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student_university', to='UniversitiesApp.University'),
        ),
    ]
