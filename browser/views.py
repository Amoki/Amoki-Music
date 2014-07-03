from django.shortcuts import render
from browser.models import Category, Music, Player


def home(request):
    player = Player.load()

    if request.method == "POST":
        if request.POST.get('add_url'):
            player.push(url=request.POST.get('url'), category=Category.objects.get(pk=request.POST.get('category')))

        if request.POST.get('play_next'):
            player.play_next()

    playing = player.actual
    categories = Category.objects.all().order_by('name')
    urls = Music.objects.all()
    time_left = player.get_remaining_time()
    count_left = player.get_number_remaining()
    nexts_music = player.get_musics_remaining()
    return render(request, 'index.html', locals())


def play(request):
    player = Player.load()
    player.play_next()
    return render(request, 'index.html')


def reset_playlist(request):
    player = Player.load()
    player.reset()
    return render(request, 'index.html')


def now_playing(request):
    player = Player.load()
    playing = player.actual
    return render(request, 'nowplaying.html', locals())
