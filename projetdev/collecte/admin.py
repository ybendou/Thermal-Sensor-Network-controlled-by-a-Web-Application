from django.contrib import admin
from .models import Room,Capteur,Temperature
# Register your models here.
admin.site.register(Room)
admin.site.register(Capteur)
admin.site.register(Temperature)
