# Generated by Django 5.1.2 on 2024-11-01 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EMS', '0010_alter_comment_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventdata',
            name='geast_list',
            field=models.EmailField(max_length=254),
        ),
    ]
