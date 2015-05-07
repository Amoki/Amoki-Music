# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from player.models import Room


def host(request):
    if not request.session.get('room', False) or not Room.objects.filter(name=request.session.get('room')).exists():
        return redirect('logout', permanent=True)
    else:
        room = Room.objects.get(name=request.session.get('room'))
        current_music = room.current_music
        if current_music:
            current_time_past = room.get_current_time_past()
            music_id = current_music.music_id
            source = current_music.source
            if current_music.timer_end:
                current_music_timer_end = current_music.timer_end

    return render(request, 'player.html', locals())
