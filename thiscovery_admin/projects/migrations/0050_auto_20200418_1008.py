# Generated by Django 3.0 on 2020-04-18 10:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0049_auto_20200407_1242'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usertask',
            old_name='url',
            new_name='user_task_url',
        ),
    ]
