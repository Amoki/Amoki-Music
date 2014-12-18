# -*- coding: utf-8 -*-
from django.shortcuts import render

from player.models import Room


def home(request):
    room_name = request.POST.get('room')
    password = request.POST.get('password')
    if request.method == "POST" and room_name and password:
        room = Room.objects.filter(name=room_name)
        if room.count() == 0:
            bad_password = True
            logging = True
        elif room[0].password != password:
            bad_password = True
            logging = True
        else:
            request.session['room'] = room_name
            request.session['token'] = room[0].token

    if not request.session.get('room', False):
        rooms = Room.objects.values_list('name', flat=True).all()
        return render(request, 'login.html', locals())

    room = Room.objects.get(name=request.session.get('room'))

    # The object Music playing
    current_music = room.current_music

    # Objects of musics in queue
    nexts_music = room.get_musics_remaining()
    # The number of music in queue
    count_left = room.get_count_remaining()
    # Total time of current music in hh:mm:ss
    if current_music:
        current_total_time = current_music.duration
        video_url = current_music.url

    # Remaining time of the queue in hh:mm:ss
    time_left = room.get_remaining_time()
    # Remaining time of the Music playing in hh:mm:ss
    current_time_left = room.get_current_remaining_time()
    # The current state of the shuffle. Can be True ou False
    shuffle = room.shuffle

    # Percent of current music time past
    if current_music:
        room.get_current_time_past_percent

    # TODO Do not return locals
    return render(request, 'index.html', locals())
