# Generated by Django 2.0.4 on 2018-05-16 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collecte', '0003_auto_20180424_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temperature',
            name='temp',
            field=models.FloatField(),
        ),
    ]