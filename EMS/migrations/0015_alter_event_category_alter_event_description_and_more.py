# Generated by Django 5.1.2 on 2024-11-02 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EMS', '0014_remove_eventdata_venue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='category',
            field=models.CharField(choices=[('private', 'Private'), ('public', 'Public')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(null=True, upload_to='event_images/'),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='ticket_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='eventdata',
            name='category',
            field=models.CharField(choices=[('private', 'Private'), ('public', 'Public')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='eventdata',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='eventdata',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='eventdata',
            name='end_time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='eventdata',
            name='geast_list',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='eventdata',
            name='image',
            field=models.ImageField(null=True, upload_to='event_images/'),
        ),
        migrations.AlterField(
            model_name='eventdata',
            name='instructions',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='eventdata',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='eventdata',
            name='place_info',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='eventdata',
            name='schedule_plan',
            field=models.ImageField(null=True, upload_to='schedule_plan_images/'),
        ),
        migrations.AlterField(
            model_name='eventdata',
            name='sitting_plan',
            field=models.ImageField(null=True, upload_to='sitting_plan_images/'),
        ),
        migrations.AlterField(
            model_name='eventdata',
            name='start_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='eventdata',
            name='start_time',
            field=models.TimeField(null=True),
        ),
    ]
