from django.shortcuts import render
from browser.models import Category, Music, Player
from browser.helpers import get_youtube_id
import datetime


def home(request):
    if request.method == "POST":
        if request.POST.get('add_url'):
            Player.push(video_id=get_youtube_id(request.POST.get('url')), category=Category.objects.get(pk=request.POST.get('category')))

        if request.POST.get('play_next'):
            Player.play_next()

        if request.POST.get('add_category'):
            Category(name=request.POST.get('category')).save()

    playing = Player.actual
    musics = Music.get_unique()
    categories = Category.objects.all().order_by('name')
    count_left = Player.get_number_remaining()
    nexts_music = Player.get_musics_remaining()
    time_left = str(datetime.timedelta(seconds=Player.get_remaining_time()))
    actual_time_left = str(datetime.timedelta(seconds=Player.get_actual_remaining_time()))
    return render(request, 'index.html', locals())
