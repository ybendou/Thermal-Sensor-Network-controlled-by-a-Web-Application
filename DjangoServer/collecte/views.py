from django.shortcuts import render

from django.http import HttpResponse
from collecte.models import Room, Capteur
from collecte.models import Temperature
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import AddRoomForm, DeleteRoomForm, ChangeCaptorRoomForm, DeleteCaptorForm
from datetime import timedelta


# Create your views here.

def welcome(req):
    return render(req,'collecte/welcomePage.html')
#Recherche des batiments
def search(req,batiment):
	room_list = Room.objects.filter(batiment=batiment).order_by('room_number')
	if len(room_list)!= 0 :
		return render(req, 'collecte/batiment.html', {'room_list': room_list,'batiment':batiment})
	return render(req,'collecte/pageIntrouvable.html')

#Liste de toutes les chambres de la maisel
def liste(req):
	room_list = Room.objects.all().order_by('-batiment','room_number')
	content={'room_list':room_list}		
	return render(req, 'collecte/list.html',content)
		
#Affiche une chambre et les températures qui lui sont associées
def room_temps(req,batiment,room_number):
	room_list=Room.objects.filter(batiment=batiment,room_number=room_number)
	if len(room_list)!=0:
		chart_temp=[]
		room=room_list[0]
		temp_list=Temperature.objects.filter(room=room).order_by('-date')
		for temp in temp_list.reverse():
			str_temp_date=str(temp.date+timedelta(hours=2))
			chart_temp_date=str_temp_date[5:7]+" "+str_temp_date[8:10]+" "+str_temp_date[:4]+" "+str_temp_date[11:16]
			chart_temp=chart_temp+[{"date":chart_temp_date,"Température":temp.temp}]
		return render(req, 'collecte/roomTemps.html',{'room':room,'temp_list':temp_list,'chart_temp':chart_temp})
	return render(req,'collecte/pageIntrouvable.html')

#Affiche la liste des capteurs, une authentification est requise
@login_required
def liste_capteurs(req):
	capteur_list=Capteur.objects.all().order_by('identifiant')

	return render(req, 'collecte/listCapteurs.html',{'capteur_list':capteur_list})


#Reçoit un message crypé (Url commençant par send/), le décrypte et prélève la température reçu par un capteur
def receive(req,message):
    
    decrypted_message=vig(txt=message,typ='d')
    if decrypted_message[:9]=="send_temp":
            identifiant=decrypted_message[10]
            temperature_string=decrypted_message[12:17]
            try:
                temperature=float(temperature_string)
                if 0<temperature<50:
                    capteurs_list=Capteur.objects.all()
                    identifiant_list=[]
                    capteur=Capteur.objects.get(identifiant=identifiant)
                    room=capteur.room
                    temp=Temperature()
                    temp.temp=temperature
                    temp.room=room
                    temp.date=timezone.now()
                    temp.save()
                return HttpResponse('thank you')
            except:
                return HttpResponse('Error404')
    else : 
        return HttpResponse('Error404')

#Rajoute une chambre via un form
@login_required	
def addRoom(req):
    

    # If this is a POST request then process the Form data
    if req.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = AddRoomForm(req.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            room=Room()
            room.batiment = form.cleaned_data['add_room_building']
            room.room_number=form.cleaned_data['add_room_number']
            room.save()

            # redirect to a new URL:
            return HttpResponse("La chambre "+str(room.room_number)+"au batiment "+str(room.batiment)+"a été rajoutée" )

    # If this is a GET (or any other method) create the default form.
    else:
        form = AddRoomForm()
        return render(req, 'collecte/add_room_form.html', {'form': form})
#Supprime une chambre via un form
@login_required	
def deleteRoom(req):
    

    # If this is a POST request then process the Form data
    if req.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = DeleteRoomForm(req.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            
            batiment = form.cleaned_data['delete_room_building']
            room_number=form.cleaned_data['delete_room_number']
            room_list=Room.objects.filter(batiment=batiment,room_number=room_number)
            if len(room_list)!= 0 :
            	room=room_list[0]
            	temp_list=Temperature.objects.filter(room=room)
            	for temp in temp_list:
            		temp.delete()
            	capteurs_list=Capteur.objects.filter(room=room)
            	if len(capteurs_list)==0:
            		room.delete()
            		return HttpResponse("The room has been deleted")
            	else:
            		return HttpResponse("This room is connected to a captor, please change the captor's room first")
            else:
            	return HttpResponse("Cette chambre "+str(batiment)+"n'existe pas")
			         
    # If this is a GET (or any other method) create the default form.
    else:
        form = DeleteRoomForm()
        room_list=Room.objects.all().order_by('-batiment')
        return render(req, 'collecte/delete_room_form.html', {'form': form,'room_list':room_list})
#Rajoute un capteur ou lui affecte une nouvelle chambre via un form
@login_required	
def changeCaptorRoom(req):
    

    # If this is a POST request then process the Form data
    if req.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = ChangeCaptorRoomForm(req.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            identifiant = form.cleaned_data['identifiant_captor']
            batiment = form.cleaned_data['room_building']
            room_number=form.cleaned_data['room_number']
            room_list=Room.objects.filter(batiment=batiment,room_number=room_number)
            if len(room_list)!=0:
            	room=room_list[0]
            	capteur_global_list=Capteur.objects.all()
            	for capteur in capteur_global_list:
            		if capteur.room==room:
            			return HttpResponse("Cette chambre a deja un capteur qui lui est affecté")
            	capteur_list=Capteur.objects.filter(identifiant=identifiant)		
            	if len(capteur_list)!=0:
            		capteur=capteur_list[0]
            		capteur.room=room
            		capteur.save()
            		return HttpResponse("Le capteur" + str(identifiant) + "a été affecté à la chambre :" + str(room_number)+ "batiment : " + batiment)
           		
            	else :
            		capteur=Capteur()
            		capteur.identifiant=identifiant
            		capteur.room=room
            		capteur.save()
            		return HttpResponse("Le capteur" + str(identifiant) + "a été crée et affecté à la chambre :" + str(room_number)+ "batiment : " + batiment)

            return HttpResponse("Veuillez rajouter la chambre avant")
			         
    # If this is a GET (or any other method) create the default form.
    else:
        form = ChangeCaptorRoomForm()
        capteur_list=Capteur.objects.all().order_by('identifiant')
        room_list=Room.objects.all().order_by('-batiment')
        return render(req, 'collecte/change_captor_room_form.html', {'form': form,'capteur_list':capteur_list,'room_list':room_list})        
#Supprime un capteur via un form
@login_required	
def deleteCaptor(req):
    

    # If this is a POST request then process the Form data
    if req.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = DeleteCaptorForm(req.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            identifiant = form.cleaned_data['identifiant_captor']                                
            capteur_list=Capteur.objects.filter(identifiant=identifiant)
            if len(capteur_list)!=0 :
            	capteur=capteur_list[0]
            	capteur.delete()
            	return HttpResponse("Le capteur" + str(identifiant) + "a été supprimé.")
            else :
            	return HttpResponse("Le capteur" + str(identifiant) + "n'existe pas")
			         
    # If this is a GET (or any other method) create the default form.
    else:
        form = DeleteCaptorForm()
        capteur_list=Capteur.objects.all().order_by('identifiant')
        return render(req, 'collecte/delete_captor_form.html', {'form': form,'capteur_list':capteur_list})     

#Decrypte un message crypté en vigenere cypher
def vig(txt='', key='projetdev09', typ='d'):
    
    k_len = len(key)
    k_ints = [ord(i) for i in key]
    txt_ints = [ord(i) for i in txt]
    ret_txt = ''
    for i in range(len(txt_ints)):
        adder = k_ints[i % k_len]
        if typ == 'd':
            adder *= -1

        v = (txt_ints[i] - 32 + adder) % 95
        ret_txt += chr(v + 32)
    return ret_txt   
'''
@login_required
def add_room(req, batiment, room_number):
    room = Room()
    room.batiment = batiment
    room.room_number = room_number
    room.save()
    return HttpResponse("Chambre ajoutée: " + str(room_number) + "batiment : " + batiment)'''
'''
@login_required
def add_temp(req,batiment,room_number,temperature):
    
    room_list=Room.objects.filter(batiment=batiment,room_number=room_number)
    if len(room_list)!=0:
        room=room_list[0]
        temp=Temperature()
        temp.temp=temperature
        temp.room=room
        temp.date=timezone.now()
        temp.save()

        return HttpResponse("Temperature prélevée : " + str(temperature) + "dans la chambre : " + str(room_number) + "au batiment : " + batiment + "le" + str(temp.date))
    
    return HttpResponse("Veuillez rajouter la chambre avant")
'''
'''
@login_required
def change_capteur_room(req,identifiant,batiment,room_number):

    room_list=Room.objects.filter(batiment=batiment,room_number=room_number)
    if len(room_list)!=0:
        room=room_list[0]
        capteur_list=Capteur.objects.filter(identifiant=identifiant)        
        if len(capteur_list)!=0:
            capteur=capteur_list[0]
            capteur.room=room
            capteur.save()
        else :
            capteur=Capteur()
            capteur.identifiant=identifiant
            capteur.room=room
            capteur.save()
        return HttpResponse("Le capteur" + str(identifiant) + "a été affecté à la chambre :" + str(room_number)+ "batiment : " + batiment)
    return HttpResponse("Veuillez rajouter la chambre avant")'''
'''
@login_required
def delete_room(req,batiment,room_number):
    room_list=Room.objects.filter(batiment=batiment,room_number=room_number)
    if len(room_list)!= 0 :
        room=room_list[0]
        temp_list=Temperature.objects.filter(room=room)
        for temp in temp_list:
            temp.delete()
        capteurs_list=Capteur.objects.filter(room=room)
        if len(capteurs_list)==0:
            room.delete()
            return HttpResponse("The room has been deleted")
        return HttpResponse("This room is connected to a captor, please change the captor's room first")
    else:
        return("The room doesn't exist")'''
'''
@login_required
def user_interface_add_room(req):
    return render(req,'collecte/user_interface_add_room.html')'''
'''
def send_temp(req,identifiant,temperature):
    capteur=Capteur.objects.get(identifiant=identifiant)
    room=capteur.room
    temp=Temperature()
    temp.temp=temperature
    temp.room=room
    temp.date=timezone.now()
    temp.save()
    return HttpResponse(str(temperature)+" °C prévelevée dans la chambre : "+str(room.room_number)+"batiment"+room.batiment)
'''
'''@login_required
def user_interface(req):
    return render(req,'collecte/user_interface.html')'''