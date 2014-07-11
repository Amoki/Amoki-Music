from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from browser.models import Music, Player
from browser.helpers import get_youtube_id
import datetime


@csrf_exempt
def home(request):
    malform = False

    if request.method == "POST":
        if request.POST.get('url'):
            video_id = get_youtube_id(request.POST.get('url'))
            if video_id == "":
                malform_url = True
            else:
                Player.push(video_id)
        if request.POST.get('play_next'):
            Player.play_next()
        return HttpResponseRedirect(reverse("browser.views.home"))

    playing = Player.actual
    musics = Music.get_unique()
    count_left = Player.get_number_remaining()
    nexts_music = Player.get_musics_remaining()
    time_left = str(datetime.timedelta(seconds=Player.get_remaining_time()))
    actual_time_left = str(datetime.timedelta(seconds=Player.get_actual_remaining_time()))

    return render(request, 'index.html', locals())
