# Generated by Django 2.0.4 on 2018-04-24 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collecte', '0002_capteur'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temperature',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
