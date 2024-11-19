# Generated by Django 5.1.3 on 2024-11-18 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EMS', '0023_eventdata_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventdata',
            name='art_category',
            field=models.CharField(blank=True, choices=[('music', 'Music'), ('nightlife', 'Nightlife'), ('performingVisualArts', 'Performing & Visual Arts'), ('holidays', 'Holidays'), ('dating', 'Dating'), ('hobbies', 'Hobbies'), ('business', 'Business'), ('foodDrink', 'Food & Drink'), ('other', 'Other')], default='other', max_length=20),
        ),
        migrations.AlterField(
            model_name='eventdata',
            name='link',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]