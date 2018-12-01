# Generated by Django 2.0.4 on 2018-04-22 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collecte', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Capteur',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifiant', models.IntegerField()),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collecte.Room')),
            ],
        ),
    ]
