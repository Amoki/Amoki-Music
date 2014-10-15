# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from player.models import Music, Player
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

    # Remaining time of the queue in hh:mm:ss
    time_left = Player.get_remaining_time()
    # Remaining time of the Music playing in hh:mm:ss
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
def search_youtube(request):
    if request.is_ajax():
        json_data = regExp(url=request.POST.get('url'), input='search-youtube')
        return HttpResponse(json_data, content_type='application/json')
    return redirect('/')


@csrf_exempt
def lien_mort(request):
    Player.signal_lien_mort()
    return redirect('/')


def regExp(**kwargs):
    regExped = False
    if kwargs['url'] is None or kwargs['url'] == "":
        data = Music.objects.all()
    else:
        if kwargs['input'] == "search":
            regex = re.compile("(((\?v=)|youtu\.be\/)(.){11})$", re.IGNORECASE | re.MULTILINE)
            if regex.search(kwargs['url']) is None:
                data = Music.search(string=kwargs['url'])
            else:
                Player.push(video_id=youtube.get_id(kwargs['url']))
                data = Music.objects.filter(video_id=youtube.get_id(kwargs['url']))
                regExped = True
        else:
            Player.push(video_id=youtube.get_id(kwargs['url']))
            data = Music.objects.filter(video_id=youtube.get_id(kwargs['url']))
            regExped = False
    model_json = serializers.serialize('json', data, fields=('video_id', 'name', 'thumbnail', 'count'))
    list_json = json.loads(model_json)
    json_data = json.dumps({'music': list_json, 'regExp': regExped})
    return json_data
