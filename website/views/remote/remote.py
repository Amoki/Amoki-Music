# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template.loader import render_to_string

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from website.decorators import room_required
from website.json_renderer import JSONResponse

from music.serializers import MusicSerializer


@api_view(['POST'])
@room_required
def volume_change(request, room):
    if room.current_music:
        if request.data.get('volume_change') == 'up':
            room.increase_volume()
        else:
            room.decrease_volume()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response("No current music", status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@room_required
def trigger_shuffle(request, room):
    if not request.data.get('shuffle') or room.music_set.count() == 0:
        return Response("Shuffle is not allowed or no available music in this room", status=status.HTTP_400_BAD_REQUEST)

    room.toggle_shuffle((request.data.get('shuffle') == 'true'))
    remote_template_rendered = render_remote(room=room)
    return JSONResponse(remote_template_rendered)


@api_view(['POST'])
@room_required
def next_music(request, room):
    if not room.current_music:
        return Response("Can't skip music: there is no current music", status=status.HTTP_409_CONFLICT)
    if request.data.get('music_id') == room.current_music.music_id:
        room.play_next()
    remote_template_rendered = render_remote(room)
    return JSONResponse(remote_template_rendered)


@api_view(['DELETE'])
@room_required
def remove_music(request, room):
    if request.data.get('music_id') == room.current_music.music_id:
        room.signal_dead_link()
        room.play_next()
    player_template_rendered = render_remote(room)
    return JSONResponse(player_template_rendered)


@api_view(['POST'])
@room_required
def update_remote(request, room):
    musics = room.music_set.filter(dead_link=False).exclude(last_play__isnull=True).order_by('-last_play')
    paginator = Paginator(musics, 16)
    more_musics = False
    try:
        page = int(request.data.get('page'))
    except ValueError:
        page = 1
    try:
        musics = []
        for i in range(1, page + 1):
            musics += paginator.page(i).object_list
        if(paginator.page(page).has_next()):
            more_musics = True
        else:
            more_musics = False
    except (InvalidPage, EmptyPage):
        return Response("Error while refreshing the library, please reload the page", status=status.HTTP_409_CONFLICT)

    remote_updated = render_remote(room)
    remote_updated['template_library'] = render_to_string("include/remote/library.html", {
        "musics": musics,
        "tab": "library-list-music",
        "moreMusics": more_musics
    })
    remote_updated['moreMusics'] = more_musics

    return JSONResponse(remote_updated)


def render_remote(room):
    if room.current_music:
        current_music = MusicSerializer(room.current_music).data
    else:
        current_music = None

    shuffle_state = room.shuffle

    template_playlist = render_to_string("include/remote/playlist.html", {
        "playlist": room.get_musics_remaining(),
        "shuffle": shuffle_state
    })
    template_header_remote = render_to_string("include/remote/header_remote.html", {
        "current_music": room.current_music
    })
    current_time_left = room.get_current_remaining_time()

    current_time_past = room.get_current_time_past()

    current_time_past_percent = room.get_current_time_past_percent()

    return {
        'currentMusic': current_music,
        'shuffle': shuffle_state,
        'templatePlaylist': template_playlist,
        'templateHeaderRemote': template_header_remote,
        'currentTimeLeft': current_time_left,
        'currentTimePast': current_time_past,
        'currentTimePastPercent': current_time_past_percent,
    }
