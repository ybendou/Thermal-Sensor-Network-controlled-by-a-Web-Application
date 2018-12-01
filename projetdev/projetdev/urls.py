"""projetdev URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from collecte.views import *
from django.conf.urls import include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',welcome),
    #path('collecte/add_room/<str:batiment>/<int:room_number>/', add_room),
    path('collecte/search/<str:batiment>/', search),
    path('liste/',liste),
    #path('collecte/add_temp/<str:batiment>/<int:room_number>/<int:temperature>/',add_temp),
    path('collecte/room_temps/<str:batiment>/<int:room_number>',room_temps),
    #path('collecte/change_capteur_room/<int:identifiant>/<str:batiment>/<int:room_number>',change_capteur_room),
    #path('collecte/send_temp/<int:identifiant>/<int:temperature>',send_temp),
    path('collecte/liste_capteurs',liste_capteurs),
    #path('collecte/delete_room/<str:batiment>/<int:room_number>',delete_room),
    path('accounts/', include('django.contrib.auth.urls')),
    #path('user_interface/',user_interface),
    #path('user_interface_add_room',user_interface_add_room),
    path('addRoom', addRoom, name='add-room'),
    path('deleteRoom', deleteRoom, name='delete-room'),
    path('changeCaptorRoom',changeCaptorRoom,name='change-captor-room'),
    path('deleteCaptor',deleteCaptor,name='delete-captor'),
    path('collecte/send/<str:message>',receive),

]