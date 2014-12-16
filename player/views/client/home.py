# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from models import Room


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
    if request.method == "POST":
        if request.POST.get('play_next'):
            room.play_next()
        if request.POST.get('volume_up'):
            room.increase_volume()
        if request.POST.get('volume_down'):
            room.decrease_volume()
        if request.POST.get('shuffle'):
            room.shuffle = (request.POST.get('shuffle') == 'true')
            if room.shuffle and not room.current_music:
                room.play_next()
        return HttpResponseRedirect(reverse("player.views.client.home"))

    # The object Music playing
    current_music = room.current_music
    # All objects Music
    # list_musics = Music.objects.all()

    # Objects of musics in queue
    nexts_music = room.get_musics_remaining()
    # The number of music in queue
    count_left = room.get_count_remaining()
    # Total time of current music in hh:mm:ss
    if current_music:
        current_total_time = int(current_music.duration)
        video_url = current_music.url

    # Remaining time of the queue in hh:mm:ss
    time_left = room.get_remaining_time()
    # Remaining time of the Music playing in hh:mm:ss
    current_time_left = room.get_current_remaining_time()
    # The current state of the shuffle. Can be True ou False
    shuffle = room.shuffle

    # Percent of current music time past
    if current_music:
        current_time_past_percent = ((current_total_time - current_time_left) * 100) / current_total_time

    # TODO Do not return locals
    return render(request, 'index.html', locals())
