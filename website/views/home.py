from django.shortcuts import render


def remote(request):
    return render(request, 'index.html')


def player(request):
    return render(request, 'player.html')
