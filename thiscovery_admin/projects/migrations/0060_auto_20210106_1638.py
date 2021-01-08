# Generated by Django 3.1.4 on 2021-01-06 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0059_auto_20210106_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='project_page_url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='projecttask',
            name='task_page_url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]