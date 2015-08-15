# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template.loader import render_to_string
from rest_framework.decorators import api_view

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
        return HttpResponse(204)
    return HttpResponse(404)


@api_view(['POST'])
@room_required
def trigger_shuffle(request, room):
    if not request.data.get('shuffle') or room.music_set.count() == 0:
        return HttpResponse(409)

    room.toggle_shuffle((request.data.get('shuffle') == 'true'))
    remote_template_rendered = render_remote(room=room)
    return JSONResponse(remote_template_rendered)


@api_view(['POST'])
@room_required
def next_music(request, room):
    if request.data.get('music_id') == room.current_music.music_id:
        room.play_next()
    remote_template_rendered = render_remote(room=room)
    return JSONResponse(remote_template_rendered)


@api_view(['DELETE'])
@room_required
def remove_music(request, room):
    if request.data.get('music_id') == room.current_music.music_id:
        room.signal_dead_link()
        room.play_next()
    player_template_rendered = render_remote(room=room)
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
        return HttpResponse("Error while refreshing the library, please reload the page", status=409)

    remote_updated = render_remote(room)
    remote_updated['template_library'] = render_to_string("include/remote/library.html", {
        "musics": musics,
        "tab": "library-list-music",
        "more_musics": more_musics
    })
    remote_updated['more_musics'] = more_musics

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
        'current_music': current_music,
        'shuffle': shuffle_state,
        'template_playlist': template_playlist,
        'template_header_remote': template_header_remote,
        'current_time_left': current_time_left,
        'current_time_past': current_time_past,
        'current_time_past_percent': current_time_past_percent,
    }
