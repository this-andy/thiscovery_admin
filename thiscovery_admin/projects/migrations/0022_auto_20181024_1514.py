# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-24 15:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0021_auto_20181024_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='visibility',
            field=models.CharField(blank=True, choices=[('public', 'Public'), ('private', 'Private')], max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='projecttask',
            name='visibility',
            field=models.CharField(blank=True, choices=[('public', 'Public'), ('private', 'Private')], max_length=12, null=True),
        ),
    ]
