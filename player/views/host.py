# -*- coding: utf-8 -*-
from django.shortcuts import render
from player.models import Room


def host(request):
    room_name = request.POST.get('room')
    password = request.POST.get('password')
    if request.method == "POST" and room_name and password:
        room = Room.objects.filter(name=room_name)
        if room.count() == 0:
            bad_password = True
        elif room[0].password != password:
            bad_password = True
        else:
            request.session['room'] = room_name
            request.session['token'] = room[0].token

    if not request.session.get('room', False):
        rooms = Room.objects.values_list('name', flat=True).all()
        return render(request, 'login.html', locals())
    else:
        room = Room.objects.get(name=request.session.get('room'))
        current_music = room.current_music
        if current_music:
            current_time_past = room.get_current_time_past()
            music_id = current_music.music_id

    return render(request, 'player.html', locals())


def logout(request):
    request.session.flush()
    rooms = Room.objects.values_list('name', flat=True).all()
    return render(request, 'login.html', locals())
