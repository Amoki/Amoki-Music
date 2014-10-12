# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from player.models import Music, Player
from player.helpers import get_youtube_id, increase_volume, decrease_volume, get_youtube_link


def home(request):

    if request.method == "POST":
        if request.is_ajax():
            if request.POST.get('url'):
                musics = Music.search(request.POST.get('url'))
                return HttpResponse(musics)
        
        if request.POST.get('url'):
            #list_musics = Music.search(string=request.POST.get('url'))
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

def test_post(request):
    if request.is_ajax():
        string = request.POST.get('url')
        if string == None or string == "":
            data = ''
        else:
            data = Music.search(string=request.POST.get('url'))
        return HttpResponse(json.dumps(data), content_type='application/json')
    return redirect('/')