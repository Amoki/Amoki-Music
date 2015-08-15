# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core import serializers

from player.models import Room

import simplejson as json

def update_player(request):
    if request.is_ajax and request.session.get('room', False):
        room = Room.objects.get(name=request.session.get('room'))

        template_playlist = render_to_string("include/remote/playlist.html", {
            "playlist": room.get_musics_remaining(),
            "shuffle": room.shuffle
        })

        if room.current_music:
            model_json = serializers.serialize('json', [room.current_music], fields=('music_id', 'duration'))
            current_music_json = json.loads(model_json)
        else:
            current_music_json = None


        json_data = json.dumps({
            'current_music': current_music_json,
            'template_playlist': template_playlist,
        })

        return HttpResponse(json_data, content_type='application/json')
    return redirect('/')
