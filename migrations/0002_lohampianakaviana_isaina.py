# Generated by Django 3.2.9 on 2022-12-28 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paroasy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lohampianakaviana',
            name='isaina',
            field=models.IntegerField(default=1),
        ),
    ]
