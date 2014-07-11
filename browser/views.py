# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from browser.models import Music, Player
from browser.helpers import get_youtube_id
import datetime


@csrf_exempt
def home(request):

    if request.method == "POST":
        if request.POST.get('url'):
            Player.push(video_id=get_youtube_id(request.POST.get('url')))
        if request.POST.get('play_next'):
            Player.play_next()
        if request.POST.get('shuffle'):
            Player.shuffle = request.POST.get('shuffle')
            print "shufle is now: " + Player.shuffle
            if Player.shuffle and not Player.actual:
                Player.play_next()
        return HttpResponseRedirect(reverse("browser.views.home"))

    # The object Music playing
    playing = Player.actual
    # All objects Music
    musics = Music.objects.all()
    # Objects of musics in queue
    nexts_music = Player.get_musics_remaining()
    # The number of music in queue
    count_left = Player.get_count_remaining()
    # Remaining time of the queue in hh:mm:ss
    time_left = str(datetime.timedelta(seconds=Player.get_remaining_time()))
    # Remaining time of the Music playing in hh:mm:ss
    actual_time_left = str(datetime.timedelta(seconds=Player.get_actual_remaining_time()))
    # The actual state of the suffle. Can be True ou False
    shuffle = Player.shuffle

    return render(request, 'index.html', locals())
