# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-08 05:49
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ProjectsApp', '0009_project_created_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectComment',
            fields=[
                ('comment_id', models.AutoField(primary_key=True, serialize=False)),
                ('comment', ckeditor.fields.RichTextField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ProjectsApp.Project')),
            ],
        ),
    ]
