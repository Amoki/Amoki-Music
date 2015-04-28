# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.http import HttpResponse
from django.core import serializers
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template.loader import render_to_string

from player.models import Room

import simplejson as json


def volume_change(request):
    if request.is_ajax():
        room = Room.objects.get(name=request.session.get('room'))
        if request.POST.get('volume_change') == 'up':
            room.increase_volume()
        else:
            room.decrease_volume()
        return HttpResponse('{}', content_type='application/json')
    return redirect('/')


def trigger_shuffle(request):
    if request.is_ajax and request.session.get('room', False) and request.POST.get('shuffle'):
        room = Room.objects.get(name=request.session.get('room'))
        if room.music_set.count() == 0:
            return HttpResponse(json.dumps({"error": True}), content_type='application/json')
        room.toggle_shuffle((request.POST.get('shuffle') == 'true'))

        player_template_rendered = render_remote(room=room)

        return HttpResponse(player_template_rendered, content_type='application/json')
    return redirect('/')


# Catch /next-music/ AND /dead-link/ ids
def next_music(request):
    if request.is_ajax and request.session.get('room', False):
        room = Room.objects.get(name=request.session.get('room'))
        if request.POST.get('music_id') == room.current_music.music_id:
            if request.path == "/dead-link/":
                room.signal_dead_link()
            room.play_next()
        player_template_rendered = render_remote(room=room)
        return HttpResponse(player_template_rendered, content_type='application/json')
    return redirect('/')


def update_remote(request):
    if request.is_ajax and request.session.get('room', False):
        room = Room.objects.get(name=request.session.get('room'))

        musics = room.music_set.filter(dead_link=False).order_by('-date')
        paginator = Paginator(musics, 16)
        more_musics = False
        try:
            page = int(request.POST.get('page'))
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

        player_updated = json.loads(render_remote(room))
        player_updated['template_library'] = render_to_string("include/remote/library.html", {
            "musics": musics,
            "tab": "library-list-music",
            "more_musics": more_musics
        })
        player_updated['more_musics'] = more_musics

        return HttpResponse(json.dumps(player_updated), content_type='application/json')


def render_remote(room):
    if room.current_music:
        data = room.music_set.filter(music_id=room.current_music.music_id)
        model_json = serializers.serialize('json', data, fields=('music_id', 'name', 'thumbnail', 'count', 'duration'))
        current_music = json.loads(model_json)
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

    current_time_past_percent = room.get_current_time_past_percent()

    json_data = json.dumps({
        'current_music': current_music,
        'shuffle': shuffle_state,
        'template_playlist': template_playlist,
        'template_header_remote': template_header_remote,
        'time_left': current_time_left,
        'time_past_percent': current_time_past_percent,
    })

    return json_data
