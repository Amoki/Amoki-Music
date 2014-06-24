from django.shortcuts import render
from browser.models import Category, Url, Play


def home(request):
    categories = Category.objects.all()
    urls = Url.objects.all()
    return render(request, 'index.html', locals())


def play(request):
    player = Play.load()
    player.play_next()
    return render(request, 'index.html')


def reset_playlist(request):
    player = Play.load()
    player.reset()
    return render(request, 'index.html')


def now_playing(request):
    playing = Play.load().actual
    return render(request, 'nowplaying.html', locals())
