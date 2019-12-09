# Generated by Django 2.1.7 on 2019-10-16 13:20

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0038_auto_20190809_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='usergroup',
            name='url_code',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='user',
            name='email_verification_token',
            field=models.UUIDField(default=uuid.UUID('a4e1190a-9eee-4fc7-94a1-b48030f41e99'), editable=False, null=True),
        ),
    ]