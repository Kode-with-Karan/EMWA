# Generated by Django 5.1.3 on 2024-11-30 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EMS', '0036_alter_eventdata_schedule_plan_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventdata',
            name='schedule_plan',
            field=models.ImageField(default='Schedule Plan', upload_to='schedule_plan_files/'),
        ),
    ]
