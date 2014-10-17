# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from player.models import Music, TemporaryMusic, Player
from player.helpers import youtube, volume
from django.core import serializers
import simplejson as json
import re


@csrf_exempt
def home(request):

    if request.method == "POST":
        if request.POST.get('url'):
            Player.push(video_id=youtube.get_id(request.POST.get('url')))
        if request.POST.get('play_next'):
            Player.play_next()
        if request.POST.get('volume_up'):
            volume.increase()
        if request.POST.get('volume_down'):
            volume.decrease()
        if request.POST.get('shuffle'):
            Player.shuffle = (request.POST.get('shuffle') == 'true')
            if Player.shuffle and not Player.current:
                Player.play_next()
        return HttpResponseRedirect(reverse("player.views.home"))

    # The object Music playing
    playing = Player.current
    # All objects Music
    list_musics = Music.objects.all()
    # Objects of musics in queue
    nexts_music = Player.get_musics_remaining()
    # The number of music in queue
    count_left = Player.get_count_remaining()
    # Total time of current music in hh:mm:ss
    if playing:
        current_total_time = int(playing.duration)
        video_url = youtube.get_link(playing.video_id)

    # Remaining time of the queue in hh:mm:ss
    time_left = Player.get_remaining_time()
    # Remaining time of the Music playing in hh:mm:ss
    current_time_left = Player.get_current_remaining_time()
    # The current state of the shuffle. Can be True ou False
    shuffle = Player.shuffle

    # Percent of current music time past
    if playing:
        current_time_past_percent = (((current_total_time - current_time_left) * 100) / current_total_time)

    return render(request, 'index.html', locals())


@csrf_exempt
def search_music(request):
    if request.is_ajax():
        json_data = regExp(url=request.POST.get('url'), input='search')
        return HttpResponse(json_data, content_type='application/json')
    return redirect('/')


@csrf_exempt
def add_music(request):
    if request.is_ajax():
        json_data = regExp(url=request.POST.get('video_id'), input='add-music', requestId=request.POST.get('requestId'))
        return HttpResponse(json_data, content_type='application/json')
    return redirect('/')


def regExp(**kwargs):
    regExped = False
    if kwargs['url'] is None or kwargs['url'] == "":
        query_search = []
    else:
        if kwargs['input'] == "search":
            regex = re.compile("(((\?v=)|youtu\.be\/)(.){11})$", re.IGNORECASE | re.MULTILINE)
            if regex.search(kwargs['url']) is None:
                data = youtube.search(query=kwargs['url'])
                model_json = serializers.serialize('json', data, fields=('video_id', 'name', 'thumbnail', 'count', 'duration', 'requestId'))
                query_search = json.loads(model_json)
            else:
                Player.push(video_id=youtube.get_id(kwargs['url']))
                data = Music.objects.filter(video_id=youtube.get_id(kwargs['url']))
                model_json = serializers.serialize('json', data, fields=('video_id', 'name', 'thumbnail', 'count', 'duration', 'requestId'))
                query_search = json.loads(model_json)
                regExped = True
        else:
            TemporaryMusic.clean(requestId=kwargs['requestId'])
            Player.push(video_id=youtube.get_id(kwargs['url']))
            data = Music.objects.filter(video_id=youtube.get_id(kwargs['url']))
            model_json = serializers.serialize('json', data, fields=('video_id', 'name', 'thumbnail', 'count', 'duration'))
            query_search = json.loads(model_json)
            regExped = False

    if Player.get_musics_remaining():
        model_json = serializers.serialize('json', Player.get_musics_remaining(), fields=('video_id', 'name', 'thumbnail', 'count', 'duration'))
        playlist = json.loads(model_json)
    else:
        playlist = []

    if Player.current:
        current_total_time = int(Player.current.duration)
        current_time_left = Player.get_current_remaining_time()
        current_time_past_percent = (((current_total_time - current_time_left) * 100) / current_total_time)
        json_data = json.dumps({'music': query_search, 'playlist': playlist, 'regExp': regExped, 'time_left': current_time_left, 'time_past_percent': current_time_past_percent})
    else:
        json_data = json.dumps({'music': query_search, 'playlist': playlist, 'regExp': regExped})
    
    return json_data


@csrf_exempt
def dead_link(request):
    if request.is_ajax:
        Player.signal_lien_mort()
        Player.play_next()
        json_data = data_builder()
        return HttpResponse(json_data, content_type='application/json')
    return redirect('/')


@csrf_exempt
def trigger_shuffle(request):
    if request.is_ajax:
        if request.POST.get('shuffle'):
            Player.shuffle = (request.POST.get('shuffle') == 'true')
            if Player.shuffle and not Player.current:
                Player.play_next()

            json_data = data_builder()
            return HttpResponse(json_data, content_type='application/json')
    return redirect('/')


@csrf_exempt
def next_music(request):
    if request.is_ajax:
        Player.play_next()
        json_data = data_builder()
        return HttpResponse(json_data, content_type='application/json')
    return redirect('/')


def data_builder(**kwargs):
    if Player.current:
        data = Music.objects.filter(video_id=Player.current.video_id)
        model_json = serializers.serialize('json', data, fields=('video_id', 'name', 'thumbnail', 'count', 'duration'))
        next_music = json.loads(model_json)

        data = Player.get_musics_remaining()
        model_json = serializers.serialize('json', data, fields=('video_id', 'name', 'thumbnail', 'count', 'duration'))
        playlist = json.loads(model_json)

        current = True

        current_total_time = int(Player.current.duration)
        current_time_left = Player.get_current_remaining_time()
        current_time_past_percent = (((current_total_time - current_time_left) * 100) / current_total_time)

        shuffle_state = Player.shuffle

        json_data = json.dumps({'current': current,
                                'music': next_music,
                                'playlist': playlist,
                                'time_left': current_time_left,
                                'time_past_percent': current_time_past_percent,
                                'shuffle': shuffle_state})
    else:
        current = False
        json_data = json.dumps({'current': False})
    return json_data
