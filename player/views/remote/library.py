# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template.loader import render_to_string

from player.models import Room
from player.views.remote.remote import render_remote
from music.models import Music
from music.helpers import youtube

import simplejson as json
import re


def search_music(request):
    if request.is_ajax() and request.session.get('room', False):
        regexVideoId = re.compile("(?:v=|youtu\.be\/)([^&?]+)", re.IGNORECASE | re.MULTILINE)
        if regexVideoId.search(request.POST.get('query')) is None:
            musics_searched = youtube.search(query=request.POST.get('query'))
        else:
            musics_searched = youtube.search(ids=regexVideoId.search(request.POST.get('query')).group(1), direct_link=True)
        template_library = render_to_string("include/remote/library.html", {"musics": musics_searched, "tab": "youtube-list-music"})
        json_data = json.dumps({'template_library': template_library})
        return HttpResponse(json_data, content_type='application/json')
    return redirect('/')


def add_music(request):
    if request.is_ajax() and request.session.get('room', False) and request.POST.get('music_id'):
        room = Room.objects.get(name=request.session.get('room'))
        if(request.POST.get('requestId') is None):
            music_to_add = Music.objects.get(music_id=request.POST.get('music_id'), room=room)
            room.push(
                music_id=music_to_add.music_id,
                name=music_to_add.name,
                duration=music_to_add.duration,
                thumbnail=music_to_add.thumbnail,
                timer_start=music_to_add.timer_start,
                timer_end=music_to_add.timer_end,
            )
        else:
            if request.POST.get('timer-start') is None:
                timer_start = 0
            else:
                timer_start = int(request.POST.get('timer-start'))
            room.push(
                music_id=request.POST.get('music_id'),
                requestId=request.POST.get('requestId'),
                timer_start=timer_start,
                timer_end=int(request.POST.get('timer-end')),
            )
        return HttpResponse(render_remote(room), content_type='application/json')
    return redirect('/')


def music_inifite_scroll(request):
    if request.is_ajax():
        room = Room.objects.get(name=request.session.get('room'))
        musics = room.music_set.filter(dead_link=False).order_by('-date')
        # Get the paginator
        paginator = Paginator(musics, 16)
        more_musics = False
        try:
            page = int(request.POST.get('page'))

            musics = paginator.page(page)
            if(paginator.page(page).has_next()):
                more_musics = True
            else:
                more_musics = False
        except (InvalidPage, EmptyPage, ValueError):
            return HttpResponse("Error while refreshing the library, please reload the page", status=409)

        template = render_to_string("include/remote/library.html", {"musics": musics, "tab": "library-list-music", "more_musics": more_musics})
        json_data = json.dumps({
            'template': template,
            'more_musics': more_musics
        })
        return HttpResponse(json_data, content_type="application/json")
    return redirect('/')
