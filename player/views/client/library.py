# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.http import HttpResponse
from django.core import serializers
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
    if request.is_ajax() and request.session.get('room', False):
        json_data = regExp(
            url=urllib.unquote(request.POST.get('url')),
            input='add-music',
            requestId=request.POST.get('requestId'),
            room=Room.objects.get(name=request.session.get('room'))
        )
        return HttpResponse(json_data, content_type='application/json')
    return redirect('/')


def regExp(**kwargs):
    room = kwargs['room']
    regExped = False
    if kwargs['url'] is None or kwargs['url'] == "":
        query_search = []
    else:
        if kwargs['input'] == "search":
            regex = re.compile("(v=|youtu\.be\/)([^&]*)", re.IGNORECASE | re.MULTILINE)
            if regex.search(kwargs['url']) is None:
                data = youtube.search(query=kwargs['url'])
                model_json = serializers.serialize('json', data, fields=('url', 'name', 'thumbnail', 'views', 'duration', 'requestId'))
                query_search = json.loads(model_json)
            else:
                videos = youtube.get_info(regex.search(kwargs['url']).group(2))
                if(videos):
                    room.push(
                        url=videos[0]['url'],
                        name=videos[0]['name'],
                        duration=videos[0]['duration'],
                        thumbnail=videos[0]['thumbnail'],
                    )
                    data = Music.objects.filter(url=kwargs['url'])
                    model_json = serializers.serialize('json', data, fields=('url', 'name', 'thumbnail', 'views', 'duration', 'requestId'))
                    query_search = json.loads(model_json)
                    regExped = True
        else:
            room.push(url=kwargs['url'], requestId=kwargs['requestId'])
            data = Music.objects.filter(url=kwargs['url'])
            model_json = serializers.serialize('json', data, fields=('url', 'name', 'thumbnail', 'count', 'duration'))
            query_search = json.loads(model_json)
            regExped = False

    playlist = []
    if room.get_musics_remaining():
        model_json = serializers.serialize('json', room.get_musics_remaining(), fields=('url', 'name', 'thumbnail', 'count', 'duration'))
        playlist = json.loads(model_json)

    if room.current_music:
        current_total_time = int(room.current_music.duration)
        current_time_left = room.get_current_remaining_time()
        current_time_past_percent = (((current_total_time - current_time_left) * 100) / current_total_time)
        json_data = json.dumps({'music': query_search, 'playlist': playlist, 'regExp': regExped, 'time_left': current_time_left, 'time_past_percent': current_time_past_percent})
    else:
        json_data = json.dumps({'music': query_search, 'playlist': playlist, 'regExp': regExped})

    return json_data


def music_inifi_scroll(request):
    if request.is_ajax():
        room = Room.objects.get(name=request.session.get('room'))
        musics = Music.objects.all().filter(room=room).order_by('-date')
        # Get the paginator
        paginator = Paginator(musics, 15)
        try:
            page = int(request.POST.get('page'))
        except ValueError:
            page = 1
        try:
            musics = paginator.page(page)
        except (EmptyPage, InvalidPage):
            musics = paginator.page(paginator.num_pages)

        tab = "library-list-music"

        template = render_to_string("include/library.html", {"musics": musics, "tab": tab})
        json_data = json.dumps({
            'template': template
        })
        return HttpResponse(json_data, content_type="application/json")
    return redirect('/')
