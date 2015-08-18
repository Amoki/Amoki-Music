# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view

from website.json_renderer import JSONResponse
from player.models import Room
from player.serializers import RoomSerializer
from music.serializers import MusicSerializer
from website.decorators import room_required


from music.models import Source


def home(request):
    if not request.session.get('token', False) or not Room.objects.filter(token=request.session.get('token')).exists():
        return redirect('logout', permanent=True)

    room = Room.objects.get(token=request.session.get('token'))

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
        current_music_json = MusicSerializer(current_music).data

        # Total time of current music in hh:mm:ss
        current_total_time = current_music.duration
        music_id = current_music.music_id
    else:
        current_music_json = None

    json_data = JSONRenderer().render({
        'currentMusic': current_music_json,
        'timeLeft': time_left,
        'currentTimeLeft': current_time_left,
        'currentTimePast': current_time_past,
        'currentTimePastPercent': current_time_past_percent,
    })

    # TODO Do not return locals
    return render(request, 'index.html', locals())


@api_view(['GET'])
@room_required
def room(request, room):
    return JSONResponse(RoomSerializer(room).data)
