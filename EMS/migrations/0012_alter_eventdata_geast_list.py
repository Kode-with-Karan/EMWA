# Generated by Django 5.1.2 on 2024-11-01 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EMS', '0011_alter_eventdata_geast_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventdata',
            name='geast_list',
            field=models.TextField(),
        ),
    ]
