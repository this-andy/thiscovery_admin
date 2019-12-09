from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0039_auto_20191016_1320'),
    ]

    operations = [
        migrations.RunSQL("CREATE UNIQUE INDEX email_index ON projects_user(lower(email));"),
    ]
