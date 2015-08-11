# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template.loader import render_to_string
from rest_framework.decorators import api_view

from player.views.json_renderer import JSONResponse
from music.serializers import MusicSerializer

from player.models import Room


@api_view(['POST'])
def volume_change(request):
    if request.session.get('room', False):
        room = Room.objects.get(name=request.session.get('room'))
        if request.data.get('volume_change') == 'up':
            room.increase_volume()
        else:
            room.decrease_volume()
        return JSONResponse()
    return HttpResponse(401)


@api_view(['POST'])
def trigger_shuffle(request):
    if request.session.get('room', False) and request.data.get('shuffle'):
        room = Room.objects.get(name=request.session.get('room'))
        if room.music_set.count() == 0:
            return JSONResponse({"error": True})
        room.toggle_shuffle((request.data.get('shuffle') == 'true'))

        player_template_rendered = render_remote(room=room)

        return JSONResponse(player_template_rendered)
    return HttpResponse(401)


@api_view(['POST'])
def next_music(request):
    if request.session.get('room', False):
        room = Room.objects.get(name=request.session.get('room'))
        if request.data.get('music_id') == room.current_music.music_id:
            room.play_next()
        player_template_rendered = render_remote(room=room)
        return JSONResponse(player_template_rendered)
    return HttpResponse(401)


@api_view(['DELETE'])
def remove_music(request):
    if request.session.get('room', False):
        room = Room.objects.get(name=request.session.get('room'))
        if request.data.get('music_id') == room.current_music.music_id:
            room.signal_dead_link()
            room.play_next()
        player_template_rendered = render_remote(room=room)
        return JSONResponse(player_template_rendered)
    return HttpResponse(401)


@api_view(['POST'])
def update_remote(request):
    if request.session.get('room', False):
        room = Room.objects.get(name=request.session.get('room'))

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

        player_updated = render_remote(room)
        player_updated['template_library'] = render_to_string("include/remote/library.html", {
            "musics": musics,
            "tab": "library-list-music",
            "more_musics": more_musics
        })
        player_updated['more_musics'] = more_musics

        return JSONResponse(player_updated)
    return HttpResponse(401)


def render_remote(room):
    if room.current_music:
        music = room.music_set.get(music_id=room.current_music.music_id)
        model_json = MusicSerializer(music)
        current_music = model_json.data
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
        'time_left': current_time_left,
        'time_past': current_time_past,
        'time_past_percent': current_time_past_percent,
    }
