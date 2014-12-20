# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from player.models import Room


def host(request):
	if not request.session.get('room', False):
		return redirect('login', permanent=True)
	else:
		room = Room.objects.get(name=request.session.get('room'))
		current_music = room.current_music
		if current_music:
			current_time_past = room.get_current_time_past()
			music_id = current_music.music_id

	return render(request, 'player.html', locals())
