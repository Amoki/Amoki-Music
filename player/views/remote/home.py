# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from player.models import Room
from music.models import Source


def home(request):
    if not request.session.get('room', False) or not Room.objects.filter(name=request.session.get('room')).exists():
        return redirect('logout', permanent=True)

    room = Room.objects.get(name=request.session.get('room'))

    # The object Music playing
    current_music = room.current_music

    # Objects of musics in queue
    playlist = room.get_musics_remaining()
    # The number of music in queue
    count_left = room.get_count_remaining()
    # Total time of current music in hh:mm:ss
    if current_music:
        current_total_time = current_music.duration
        music_id = current_music.music_id

    # Remaining time of the queue in hh:mm:ss
    time_left = room.get_remaining_time()
    # Remaining time of the Music playing in hh:mm:ss
    current_time_left = room.get_current_remaining_time()
    # The current state of the shuffle. Can be True ou False
    shuffle = room.shuffle

    sources = Source.objects.all()

    # Percent of current music time past
    if current_music:
        current_time_past_percent = room.get_current_time_past_percent

    # TODO Do not return locals
    return render(request, 'index.html', locals())
