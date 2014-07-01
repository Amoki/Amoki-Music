from django.shortcuts import render
from browser.models import Category, Url, Play


def home(request):
    player = Play.load()

    if request.method == "POST":
        if request.POST.get('add_url'):
            url = Url(
                url=request.POST.get('url'),
                category=Category.objects.get(pk=request.POST.get('category'))
            )
            url.save()

        if request.POST.get('play_next'):
            player = Play.load()
            player.play_next()

    player = Play.load()
    playing = player.actual
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
    player = Play.load()
    playing = player.actual
    return render(request, 'nowplaying.html', locals())
