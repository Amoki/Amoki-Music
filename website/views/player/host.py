from django.shortcuts import render, redirect
from player.models import Room


def host(request):
    if not request.session.get('room', False) or not Room.objects.filter(name=request.session.get('room')).exists():
        return redirect('logout', permanent=True)
    else:
        room = Room.objects.get(name=request.session.get('room'))
        current_music = room.current_music
        shuffle = room.shuffle
        playlist = room.get_musics_remaining()
        if current_music:
            current_time_past = room.get_current_time_past()

    return render(request, 'player.html', locals())
