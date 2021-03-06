# Generated by Django 3.0 on 2019-12-13 12:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0041_auto_20191213_1141'),
    ]

    operations = [
        migrations.AddField(
            model_name='projecttask',
            name='progress_info_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email_verification_token',
            field=models.UUIDField(default=uuid.UUID('0635c2e2-9ed3-46d1-96f7-711c7b0a84d7'), editable=False, null=True),
        ),
    ]
