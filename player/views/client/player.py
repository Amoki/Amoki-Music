# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.http import HttpResponse
from django.core import serializers
from django.template.loader import render_to_string

from models import Room
from models import Music

import simplejson as json


def volume_change(request):
    if request.is_ajax():
        room = Room.objects.get(name=request.session.get('room'))
        if request.POST.get('volume_change') == 'up':
            room.increase_volume()
        else:
            room.decrease_volume()
        return HttpResponse(json.dumps({'ok': 'ok'}), content_type='application/json')
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


def dead_link(request):
    if request.is_ajax and request.session.get('room', False):
        room = Room.objects.get(name=request.session.get('room'))
        if request.POST.get('url') == room.current_music.url:
            room.signal_dead_link()
            room.play_next()

        player_template_rendered = render_player(room=room)
        return HttpResponse(player_template_rendered, content_type='application/json')
    return redirect('/')


def next_music(request):
    if request.is_ajax and request.session.get('room', False):
        room = Room.objects.get(name=request.session.get('room'))
        if request.POST.get('url') == room.current_music.url:
            room.play_next()
        
        player_template_rendered = render_player(room=room)
        return HttpResponse(player_template_rendered, content_type='application/json')
    return redirect('/')


def render_player(room):
    data = Music.objects.filter(url=room.current_music.url)
    model_json = serializers.serialize('json', data, fields=('url', 'name', 'thumbnail', 'count', 'duration'))
    current_music = json.loads(model_json)

    data_playlist = room.get_musics_remaining()
    model_json = serializers.serialize('json', data_playlist)
    playlist = json.loads(model_json)

    shuffle_state = room.shuffle

    template_playlist = render_to_string("include/playlist.html", {
        "playlist": playlist,
        "shuffle": shuffle_state
    })
    template_header_player = render_to_string("include/header_player.html", {
        "current_music": current_music
    })
    current_time_left = room.get_current_remaining_time()

    current_time_past_percent = room.get_current_time_past_percent()

    json_data = json.dumps({
        'current': current_music,
        'playlist': playlist,
        'shuffle': shuffle_state,
        'template_playlist': template_playlist,
        'template_header_player': template_header_player,
        'time_left': current_time_left,
        'time_past_percent': current_time_past_percent,
    })
    
    return json_data


def data_builder(**kwargs):
    room = kwargs['room']
    if room.current_music:
        data = Music.objects.filter(url=room.current_music.url)
        model_json = serializers.serialize('json', data, fields=('url', 'name', 'thumbnail', 'count', 'duration'))
        next_music = json.loads(model_json)

        data = room.get_musics_remaining()
        model_json = serializers.serialize('json', data, fields=('url', 'name', 'thumbnail', 'count', 'duration'))
        playlist = json.loads(model_json)

        current_total_time = int(room.current_music.duration)
        current_time_left = room.get_current_remaining_time()
        current_time_past_percent = ((current_total_time - current_time_left) * 100) / current_total_time

        shuffle_state = room.shuffle
        playing = room.current_music
        template_playlist = render_to_string("include/playlist.html", {
            "playlist": playlist,
            "next_music": next_music,
            "shuffle": shuffle_state
        })
        template_header_player = render_to_string("include/header_player.html", {
            "playing": playing
        })

        if 'skipped' in kwargs:
            json_data = json.dumps({
                'current': True,
                'music': next_music,
                'playlist': playlist,
                'time_left': current_time_left,
                'time_past_percent': current_time_past_percent,
                'shuffle': shuffle_state,
                'skipped': kwargs['skipped']
            })
        else:
            json_data = json.dumps({
                'current': True,
                'music': next_music,
                'playlist': playlist,
                'time_left': current_time_left,
                'time_past_percent': current_time_past_percent,
                'shuffle': shuffle_state,
                'template_playlist': template_playlist,
                'template_header_player': template_header_player,
            })
    else:
        json_data = json.dumps({'current': False})
    return json_data
