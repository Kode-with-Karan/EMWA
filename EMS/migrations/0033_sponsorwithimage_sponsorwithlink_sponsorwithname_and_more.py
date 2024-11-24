# Generated by Django 5.1.3 on 2024-11-24 13:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EMS', '0032_remove_profile_additional_info'),
    ]

    operations = [
        migrations.CreateModel(
            name='SponsorWithImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(upload_to='sponsorsWithImage/logos/')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sponsorsWithImage', to='EMS.eventdata')),
            ],
        ),
        migrations.CreateModel(
            name='SponsorWithLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(upload_to='sponsorsWithLink/logos/')),
                ('link', models.URLField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sponsorsWithLink', to='EMS.eventdata')),
            ],
        ),
        migrations.CreateModel(
            name='SponsorWithName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sponsorsWithName', to='EMS.eventdata')),
            ],
        ),
        migrations.DeleteModel(
            name='Sponsor',
        ),
    ]