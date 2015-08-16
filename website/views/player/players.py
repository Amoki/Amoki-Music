# -*- coding: utf-8 -*-
from django.template.loader import render_to_string
from rest_framework.decorators import api_view
from website.json_renderer import JSONResponse
from website.decorators import room_required

from music.serializers import MusicSerializer


@api_view(['POST'])
@room_required
def update_player(request, room):
    template_playlist = render_to_string("include/remote/playlist.html", {
        "playlist": room.get_musics_remaining(),
        "shuffle": room.shuffle
    })

    if room.current_music:
        current_music = MusicSerializer(room.current_music).data
    else:
        current_music = None

    json = {
        'currentMusic': current_music,
        'templatePlaylist': template_playlist,
    }

    return JSONResponse(json)
