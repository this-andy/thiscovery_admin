# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-17 10:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_userproject_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectTask',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(default='', max_length=500)),
                ('status', models.CharField(blank=True, max_length=12, null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project')),
                ('task_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.TaskType')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
