# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template.loader import render_to_string

from player.models import Room

import simplejson as json

def update_player(request):
    if request.is_ajax and request.session.get('room', False):
        room = Room.objects.get(name=request.session.get('room'))

        template_playlist = render_to_string("include/remote/playlist.html", {
            "playlist": room.get_musics_remaining(),
            "shuffle": room.shuffle
        })

        return HttpResponse(json.dumps(template_playlist), content_type='application/json')
    return redirect('/')
