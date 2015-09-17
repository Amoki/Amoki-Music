from django.shortcuts import render, redirect
from player.models import Room


def login(request):
    if request.session.get('room', False):
        return redirect('remote', permanent=True)
    room_name = request.POST.get('room')
    password = request.POST.get('password')
    if request.method == "POST" and room_name and password:
        room = Room.objects.filter(name=room_name)
        if room.count() == 0:
            bad_room = True
        elif room[0].password != password:
            bad_password = True
        else:
            request.session['room'] = room_name
            request.session['token'] = room[0].token
            return redirect('remote', permanent=True)

    rooms = Room.objects.values_list('name', flat=True).all()
    return render(request, 'login.html', locals())


def logout(request):
    request.session.flush()
    rooms = Room.objects.values_list('name', flat=True).all()
    return render(request, 'login.html', locals())
