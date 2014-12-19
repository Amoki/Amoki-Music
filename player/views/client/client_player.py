# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.http import HttpResponse
from django.core import serializers
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
        room.shuffle = (request.POST.get('shuffle') == 'true')
        room.save()
        if room.shuffle and not room.current_music:
            room.play_next()

        player_template_rendered = render_player(room=room)

        return HttpResponse(player_template_rendered, content_type='application/json')
    return redirect('/')


# Catch /next-music/ AND /dead-link/ urls
def next_music(request):
    if request.is_ajax and request.session.get('room', False):
        room = Room.objects.get(name=request.session.get('room'))
        if request.POST.get('url') == room.current_music.url:
            if request.path == "/dead-link/":
                room.signal_dead_link()
            room.play_next()
        player_template_rendered = render_player(room=room)
        return HttpResponse(player_template_rendered, content_type='application/json')
    return redirect('/')


def update_player(request):
    if request.is_ajax and request.session.get('room', False):
        room = Room.objects.get(name=request.session.get('room'))
        player_updated = render_player(room=room)
        return HttpResponse(player_updated, content_type='application/json')


def render_player(room):
    if room.current_music:
        data = room.music_set.filter(url=room.current_music.url)
        model_json = serializers.serialize('json', data, fields=('url', 'name', 'thumbnail', 'count', 'duration'))
        current_music = json.loads(model_json)
    else:
        current_music = None

    shuffle_state = room.shuffle

    template_playlist = render_to_string("include/playlist.html", {
        "playlist": room.get_musics_remaining(),
        "shuffle": shuffle_state
    })
    template_header_player = render_to_string("include/header_player.html", {
        "current_music": room.current_music
    })
    current_time_left = room.get_current_remaining_time()

    current_time_past_percent = room.get_current_time_past_percent()

    json_data = json.dumps({
        'current_music': current_music,
        'shuffle': shuffle_state,
        'template_playlist': template_playlist,
        'template_header_player': template_header_player,
        'time_left': current_time_left,
        'time_past_percent': current_time_past_percent,
    })

    return json_data
