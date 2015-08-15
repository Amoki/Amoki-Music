# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from player.models import Room
from music.models import Source
from django.core import serializers

import simplejson as json


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

    # Remaining time of the queue in hh:mm:ss
    time_left = room.get_remaining_time()
    # Remaining time of the Music playing in hh:mm:ss
    current_time_left = room.get_current_remaining_time()
    # Value of current music time past
    current_time_past = room.get_current_time_past()
    # Percent of current music time past
    current_time_past_percent = room.get_current_time_past_percent()
    # The current state of the shuffle. Can be True ou False
    shuffle = room.shuffle

    sources = Source.objects.all()

    if current_music:
        model_json = serializers.serialize('json', [current_music], fields=('music_id', 'duration'))
        current_music_json = json.loads(model_json)

        # Total time of current music in hh:mm:ss
        current_total_time = current_music.duration
        music_id = current_music.music_id
    else:
        current_music_json = None

    json_data = json.dumps({
        'current_music': current_music_json,
        'time_left': time_left,
        'current_time_left': current_time_left,
        'current_time_past': current_time_past,
        'current_time_past_percent': current_time_past_percent,
    })

    # TODO Do not return locals
    return render(request, 'index.html', locals())
