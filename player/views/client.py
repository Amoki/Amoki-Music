# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from player.models import Room, Music
from player.helpers import youtube, volume
from django.core import serializers
import simplejson as json
import re
import urllib


@csrf_exempt
def home(request):
    room_name = request.POST.get('room')
    password = request.POST.get('password')
    if request.method == "POST" and room_name and password:
        room = Room.objects.filter(name=room_name)
        if room.count() == 0:
            bad_password = True
            logging = True
        elif room[0].password != password:
            bad_password = True
            logging = True
        else:
            request.session['room'] = room_name
            request.session.set_expiry(0)

    if not request.session.get('room', False):
        rooms = Room.objects.values_list('name', flat=True).all()
        return render(request, 'login.html', locals())

    room = Room.objects.get(name=request.session.get('room'))
    if request.method == "POST":
        if request.POST.get('play_next'):
            room.play_next()
        if request.POST.get('volume_up'):
            volume.increase()
        if request.POST.get('volume_down'):
            volume.decrease()
        if request.POST.get('shuffle'):
            room.shuffle = (request.POST.get('shuffle') == 'true')
            if room.shuffle and not room.current_music:
                room.play_next()
        return HttpResponseRedirect(reverse("player.views.client.home"))

    # The object Music playing
    playing = room.current_music
    # All objects Music
    list_musics = Music.objects.all()
    # Objects of musics in queue
    nexts_music = room.get_musics_remaining()
    # The number of music in queue
    count_left = room.get_count_remaining()
    # Total time of current music in hh:mm:ss
    if playing:
        current_total_time = int(playing.duration)
        video_url = playing.url

    # Remaining time of the queue in hh:mm:ss
    time_left = room.get_remaining_time()
    # Remaining time of the Music playing in hh:mm:ss
    current_time_left = room.get_current_remaining_time()
    # The current state of the shuffle. Can be True ou False
    shuffle = room.shuffle

    # Percent of current music time past
    if playing:
        current_time_past_percent = ((current_total_time - current_time_left) * 100) / current_total_time

    # TODO Do not return locals
    return render(request, 'index.html', locals())


@csrf_exempt
def search_music(request):
    if request.is_ajax() and request.session.get('room', False):
        json_data = regExp(
            url=request.POST.get('url'),
            input='search',
            room=Room.objects.get(name=request.session.get('room'))
        )
        return HttpResponse(json_data, content_type='application/json')
    return redirect('/')


@csrf_exempt
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
            regex = re.compile("(((\?v=)|youtu\.be\/)(.){11})$", re.IGNORECASE | re.MULTILINE)
            if regex.search(kwargs['url']) is None:
                data = youtube.search(query=kwargs['url'])
                model_json = serializers.serialize('json', data, fields=('url', 'name', 'thumbnail', 'count', 'duration', 'requestId'))
                query_search = json.loads(model_json)
            else:
                # IL NOUS MANQUE PLEIN DE DATA
                room.push(url=kwargs['url'])
                data = Music.objects.filter(url=kwargs['url'])
                model_json = serializers.serialize('json', data, fields=('url', 'name', 'thumbnail', 'count', 'duration', 'requestId'))
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


@csrf_exempt
def trigger_shuffle(request):
    if request.is_ajax and request.session.get('room', False):
        room = Room.objects.get(name=request.session.get('room'))
        if request.POST.get('shuffle'):
            room.shuffle = (request.POST.get('shuffle') == 'true')
            room.save()
            if room.shuffle and not room.current_music:
                room.play_next()

            json_data = data_builder(room=room)
            return HttpResponse(json_data, content_type='application/json')
    return redirect('/')


@csrf_exempt
def dead_link(request):
    if request.is_ajax and request.session.get('room', False):
        room = Room.objects.get(name=request.session.get('room'))
        if request.POST.get('url') == room.current_music.url:
            room.signal_dead_link()
            room.play_next()
            json_data = data_builder(skipped=True, room=room)
        else:
            json_data = data_builder(room=room)
        return HttpResponse(json_data, content_type='application/json')
    return redirect('/')


@csrf_exempt
def next_music(request):
    if request.is_ajax and request.session.get('room', False):
        room = Room.objects.get(name=request.session.get('room'))
        if request.POST.get('url') == room.current_music.url:
            room.play_next()
            json_data = data_builder(skipped=True, room=room)
        else:
            json_data = data_builder()
        return HttpResponse(json_data, content_type='application/json')
    return redirect('/')


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
                'shuffle': shuffle_state
            })
    else:
        json_data = json.dumps({'current': False})
    return json_data
