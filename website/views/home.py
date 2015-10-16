from django.shortcuts import render


def remote(request):
    return render(request, 'base.html')
