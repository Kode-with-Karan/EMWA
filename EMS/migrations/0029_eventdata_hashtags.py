# Generated by Django 5.1.3 on 2024-11-21 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EMS', '0028_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventdata',
            name='hashTags',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
