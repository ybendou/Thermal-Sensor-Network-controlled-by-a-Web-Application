from django import forms
from collecte.models import Room
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.
    
class AddRoomForm(forms.Form):
    add_room_building = forms.CharField()
    add_room_number = forms.IntegerField()
    
class DeleteRoomForm(forms.Form):
	'''room_list=Room.objects.all()
	batiment_list=[]
	batiments=[]'''
	'''room_liste_choice=[]'''
	'''for room in room_list:
		if room.batiment not in batiments:
			batiment=[room.batiment,room.batiment]
			batiments.append(room.batiment)
			batiment_list.append(batiment)'''

	delete_room_building = forms.CharField()
	'''for room in room_list:
		if room.batiment == delete_room_building:
			room_number=[room.room_number,room.room_number]
			room_liste_choice.append(room_number)'''
	delete_room_number = forms.IntegerField()

class ChangeCaptorRoomForm(forms.Form):
	identifiant_captor = forms.IntegerField()
	'''room_list=Room.objects.all()
	batiment_list=[]
	batiments=[]
	for room in room_list:
		if room.batiment not in batiments:
			batiment=[room.batiment,room.batiment]
			batiments.append(room.batiment)
			batiment_list.append(batiment)'''

	room_building = forms.CharField()
	room_number = forms.IntegerField()
    
class DeleteCaptorForm(forms.Form):
	identifiant_captor=forms.IntegerField()
