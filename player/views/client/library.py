# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template.loader import render_to_string

from player.models import Room
from player.views.client.client_player import render_player
from music.models import Music
from music.helpers import youtube

import simplejson as json
import re
import urllib


def search_music(request):
    if request.is_ajax() and request.session.get('room', False):

        room = Room.objects.get(name=request.session.get('room'))
        regexVideoId = re.compile("(v=|youtu\.be\/)([^&]*)", re.IGNORECASE | re.MULTILINE)
        if regexVideoId.search(request.POST.get('url')) is None:
            musics_searched = youtube.search(query=request.POST.get('url'))
        else:
            videos = youtube.get_info(regexVideoId.search(request.POST.get('url')).group(2))
            if(videos):
                room.push(
                    url=videos[0]['url'],
                    name=videos[0]['name'],
                    duration=videos[0]['duration'],
                    thumbnail=videos[0]['thumbnail'],
                )
                return HttpResponse(render_player(room), content_type='application/json')

        tab = "youtube-list-music"
        template_library = render_to_string("include/library.html", {"musics": musics_searched, "tab": tab})
        json_data = json.dumps({
            'template_library': template_library
        })

        return HttpResponse(json_data, content_type='application/json')
    return redirect('/')


def add_music(request):
    if request.is_ajax() and request.session.get('room', False) and request.POST.get('url'):
        room = Room.objects.get(name=request.session.get('room'))
        if(request.POST.get('requestId') == "undefined"):
            music_to_add = Music.objects.get(url=urllib.unquote(request.POST.get('url')), room=room)
            room.push(
                    url=music_to_add.url,
                    name=music_to_add.name,
                    duration=music_to_add.duration,
                    thumbnail=music_to_add.thumbnail,
            )
        else:
            room.push(url=urllib.unquote(request.POST.get('url')), requestId=request.POST.get('requestId'))
        return HttpResponse(render_player(room), content_type='application/json')
    return redirect('/')


def music_inifi_scroll(request):
    if request.is_ajax():
        room = Room.objects.get(name=request.session.get('room'))
        musics = Music.objects.filter(room=room).order_by('-date')
        # Get the paginator
        paginator = Paginator(musics, 8)
        more_musics = False
        try:
            page = int(request.POST.get('page'))
        except ValueError:
            page = 1
        try:
            musics = paginator.page(page)
            if(paginator.page(page).has_next()):
                more_musics = True
            else:
                more_musics = False
        except (EmptyPage, InvalidPage):
            musics = None

        tab = "library-list-music"

        template = render_to_string("include/library.html", {"musics": musics, "tab": tab, "more_musics": more_musics})
        json_data = json.dumps({
            'template': template,
            'more_musics': more_musics
        })
        return HttpResponse(json_data, content_type="application/json")
    return redirect('/')
