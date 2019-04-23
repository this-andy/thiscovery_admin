# Generated by Django 2.1.7 on 2019-04-22 15:45

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0036_auto_20190418_1543'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='crm_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email_verification_token',
            field=models.UUIDField(default=uuid.UUID('704a2356-6e8d-447c-ab5a-93e855355c5b'), editable=False, null=True),
        ),
    ]
