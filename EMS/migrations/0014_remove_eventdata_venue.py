# Generated by Django 5.1.2 on 2024-11-01 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EMS', '0013_eventdata_schedule_plan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventdata',
            name='venue',
        ),
    ]
