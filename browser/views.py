from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from browser.models import Music, Player
from browser.helpers import get_youtube_id
import datetime


@csrf_exempt
def home(request):
    if request.method == "POST":
        if request.POST.get('add_url'):
            print request.POST
            Player.push(video_id=get_youtube_id(request.POST.get('url')))

        if request.POST.get('play_next'):
            Player.play_next()

    playing = Player.actual
    musics = Music.get_unique()
    count_left = Player.get_number_remaining()
    nexts_music = Player.get_musics_remaining()
    time_left = str(datetime.timedelta(seconds=Player.get_remaining_time()))
    actual_time_left = str(datetime.timedelta(seconds=Player.get_actual_remaining_time()))
    return render(request, 'index.html', locals())
