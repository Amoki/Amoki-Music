from django.shortcuts import render, redirect
from rest_framework.renderers import JSONRenderer

from player.models import Room
from music.serializers import MusicSerializer

def home(request):
    if not request.session.get('token', False) or not Room.objects.filter(token=request.session.get('token')).exists():
        return redirect('logout', permanent=True)

    return render(request, 'index.html', locals())


# @api_view(['GET'])
# @room_required
# def room(request, room):
#     return JSONResponse(RoomSerializer(room).data)
