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


def search_music(request):
    if request.is_ajax() and request.session.get('room', False):
        room = Room.objects.get(name=request.session.get('room'))
        regexVideoId = re.compile("(v=|youtu\.be\/)([^&]*)", re.IGNORECASE | re.MULTILINE)
        if regexVideoId.search(request.POST.get('query')) is None:
            musics_searched = youtube.search(query=request.POST.get('query'))
        else:
            videos = youtube.get_info(regexVideoId.search(request.POST.get('query')).group(2))
            if(videos):
                room.push(
                    id=videos[0]['id'],
                    name=videos[0]['name'],
                    duration=videos[0]['duration'],
                    thumbnail=videos[0]['thumbnail'],
                )
                return HttpResponse(render_player(room), content_type='application/json')
            else:
                error = "wrong-link"
                template_library = render_to_string("include/errors.html", {"error": error})
                json_data = json.dumps({
                    'template_library': template_library
                })
                return HttpResponse(json_data, content_type='application/json')
        template_library = render_to_string("include/remote/library.html", {"musics": musics_searched, "tab": "youtube-list-music"})
        json_data = json.dumps({
            'template_library': template_library
        })

        return HttpResponse(json_data, content_type='application/json')
    return redirect('/')


def add_music(request):
    if request.is_ajax() and request.session.get('room', False) and request.POST.get('music_id'):
        room = Room.objects.get(name=request.session.get('room'))
        if(request.POST.get('requestId') == "undefined"):
            music_to_add = Music.objects.get(music_id=request.POST.get('music_id'), room=room)
            room.push(
                music_id=music_to_add.music_id,
                name=music_to_add.name,
                duration=music_to_add.duration,
                thumbnail=music_to_add.thumbnail,
            )
        else:
            room.push(music_id=request.POST.get('music_id'), requestId=request.POST.get('requestId'))

        musics = room.music_set.all().order_by('-date')
        # Get the paginator
        paginator = Paginator(musics, 16)
        more_musics = False
        try:
            page = int(request.POST.get('page')) - 1
        except ValueError:
            page = 1
            print("Error on page requested")
        try:
            musics = []
            for i in range(0, page):
                musics += paginator.page(i + 1).object_list
            if(paginator.page(page).has_next()):
                more_musics = True
            else:
                more_musics = False
        except (EmptyPage, InvalidPage):
            musics = None
        response = json.loads(render_player(room))
        response['template_library'] = render_to_string("include/remote/library.html", {"musics": musics, "tab": "library-list-music", "more_musics": more_musics})
        return HttpResponse(json.dumps(response), content_type='application/json')
    return redirect('/')


def music_inifite_scroll(request):
    if request.is_ajax():
        room = Room.objects.get(name=request.session.get('room'))
        musics = room.music_set.all().order_by('-date')
        # Get the paginator
        paginator = Paginator(musics, 16)
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

        template = render_to_string("include/remote/library.html", {"musics": musics, "tab": tab, "more_musics": more_musics})
        json_data = json.dumps({
            'template': template,
            'more_musics': more_musics
        })
        return HttpResponse(json_data, content_type="application/json")
    return redirect('/')
