# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from player.models import Music, Player
from player.helpers import get_youtube_id, increase_volume, decrease_volume, get_youtube_link
from django.core import serializers
import json

@csrf_exempt
def home(request):

    if request.method == "POST":
        if request.POST.get('url'):
            Player.push(video_id=get_youtube_id(request.POST.get('url')))
        if request.POST.get('play_next'):
            Player.play_next()
        if request.POST.get('volume_up'):
            increase_volume()
        if request.POST.get('volume_down'):
            decrease_volume()
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
        video_url = get_youtube_link(playing.video_id)

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
        string = request.POST.get('url')
        if string is None or string == "":
            data = Music.objects.all()
        else:
            data = Music.search(string=request.POST.get('url'))
        json_data = serializers.serialize('json', data, fields=('video_id','name','count'));
        return HttpResponse(json_data, content_type='application/json')
    return redirect('/')

@csrf_exempt
def add_music(request):
    if request.is_ajax():
        Player.push(video_id=get_youtube_id(request.POST.get('url')))
        nexts_music = Music.objects.filter(video_id=request.POST.get('url'))
        json_data = serializers.serialize('json', nexts_music, fields=('name, duration, thumbnail'))
        return HttpResponse(json_data, content_type='application/json')
    return redirect('/')
