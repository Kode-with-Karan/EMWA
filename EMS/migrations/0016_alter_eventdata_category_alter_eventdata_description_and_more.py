# Generated by Django 5.1.2 on 2024-11-02 10:48

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EMS', '0015_alter_event_category_alter_event_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventdata',
            name='category',
            field=models.CharField(blank=True, choices=[('private', 'Private'), ('public', 'Public')], default='public', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='eventdata',
            name='description',
            field=models.TextField(blank=True, default='description'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='eventdata',
            name='end_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='eventdata',
            name='end_time',
            field=models.TimeField(blank=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='eventdata',
            name='geast_list',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='eventdata',
            name='image',
            field=models.ImageField(blank=True, default='', upload_to='event_images/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='eventdata',
            name='instructions',
            field=models.TextField(blank=True, default='instructions'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='eventdata',
            name='name',
            field=models.CharField(blank=True, default='Event', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='eventdata',
            name='place_info',
            field=models.CharField(blank=True, default='Location', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='eventdata',
            name='schedule_plan',
            field=models.ImageField(blank=True, default='', upload_to='schedule_plan_images/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='eventdata',
            name='sitting_plan',
            field=models.ImageField(blank=True, default='', upload_to='sitting_plan_images/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='eventdata',
            name='start_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='eventdata',
            name='start_time',
            field=models.TimeField(blank=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
