# Generated by Django 5.1.3 on 2024-11-30 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EMS', '0033_sponsorwithimage_sponsorwithlink_sponsorwithname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduleimage',
            name='name',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='seatingimage',
            name='name',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
