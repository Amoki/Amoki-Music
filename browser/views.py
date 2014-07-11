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
    do_not_resend_info = False
    if request.method == "POST":
        if request.POST.get('url'):
            Player.push(video_id=get_youtube_id(request.POST.get('url')))
            do_not_resend_info = True

        if request.POST.get('play_next'):
            Player.play_next()

        if request.POST.get('suffle'):
            Player.suffle = request.POST.get('suffle')

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
    suffle = Player.suffle

    if do_not_resend_info:
        return HttpResponseRedirect(reverse("browser.views.home"))

    return render(request, 'index.html', locals())
