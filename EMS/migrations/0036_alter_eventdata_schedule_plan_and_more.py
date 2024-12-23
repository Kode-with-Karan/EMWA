# Generated by Django 5.1.3 on 2024-11-30 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EMS', '0035_remove_scheduleimage_name_remove_seatingimage_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventdata',
            name='schedule_plan',
            field=models.ImageField(blank=True, default='Schedule Plan', upload_to='schedule_plan_files/'),
        ),
        migrations.AlterField(
            model_name='eventdata',
            name='sitting_plan',
            field=models.ImageField(blank=True, default='Seating Plan', upload_to='sitting_plan_files/'),
        ),
    ]
