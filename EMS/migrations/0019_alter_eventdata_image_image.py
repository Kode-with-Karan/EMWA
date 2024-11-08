# Generated by Django 5.1.2 on 2024-11-02 12:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EMS', '0018_alter_eventdata_image_alter_eventdata_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventdata',
            name='image',
            field=models.ImageField(blank=True, upload_to='event_images/'),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='event_images/')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='EMS.event')),
            ],
        ),
    ]
