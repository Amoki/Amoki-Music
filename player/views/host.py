# -*- coding: utf-8 -*-
from django.shortcuts import render

import player.sockets

from django.contrib.sessions.models import Session
Session.objects.all().delete()


def host(request):
    if request.method == "POST" and request.POST.get('room'):
        request.session['room'] = request.POST.get('room')
        request.session.set_expiry(0)

    if not request.session.get('room', False):
        return render(request, 'join-player.html', locals())
    else:
        return render(request, 'player.html', locals())


def socketio(request):
    print "POPOPO"
