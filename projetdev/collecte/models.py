from django.db import models
from django.utils import timezone

# Create your models here.

class Room(models.Model):
	room_number = models.IntegerField()
	batiment = models.CharField(max_length=255)

class Temperature(models.Model):

	temp=models.FloatField()
	room=models.ForeignKey(Room, on_delete=models.CASCADE)
	date=models.DateTimeField()

class Capteur(models.Model):

	identifiant=models.IntegerField()
	room=models.ForeignKey(Room, on_delete=models.CASCADE)