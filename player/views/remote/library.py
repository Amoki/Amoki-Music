# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template.loader import render_to_string
from rest_framework.decorators import api_view

from player.models import Room
from player.views.remote.remote import render_remote
from player.views.json_renderer import JSONResponse

from music.models import Music, Source


@api_view(['POST'])
def search_music(request):
    if request.session.get('room', False) and request.data.get('source'):
        source = Source.objects.get(name=request.data.get('source'))

        musics_searched = source.search(query=request.data.get('query'))

        template_library = render_to_string("include/remote/library.html", {
            "musics": musics_searched,
            "tab": source.name.lower() + "-list-music",
        })
        data = {'template_library': template_library}
        return JSONResponse(data)
    return HttpResponse(401)


@api_view(['POST'])
def add_music(request):
    if request.session.get('room', False) and request.data.get('music_id'):
        room = Room.objects.get(name=request.session.get('room'))
        if not request.data.get('requestId') and request.data.get('source'):
            music_to_add = Music.objects.get(music_id=request.data.get('music_id'), room=room, source__name=request.data.get('source'))
            room.push(
                music_id=music_to_add.music_id,
                name=music_to_add.name,
                duration=music_to_add.duration,
                thumbnail=music_to_add.thumbnail,
                timer_start=music_to_add.timer_start,
                timer_end=music_to_add.timer_end,
                url=music_to_add.url,
                source=Source.objects.get(name=request.data.get('source'))
            )
        else:
            try:
                timer_end = int(request.data.get('timer-end'))
            except Exception:
                timer_end = None
            room.push(
                music_id=request.data.get('music_id'),
                requestId=request.data.get('requestId'),
                timer_start=int(request.data.get('timer-start', 0)),
                timer_end=timer_end,
            )
        return JSONResponse(render_remote(room))
    return HttpResponse(401)


@api_view(['POST'])
def music_infinite_scroll(request):
    if request.session.get('room', False):
        room = Room.objects.get(name=request.session.get('room'))
        musics = room.music_set.filter(dead_link=False).exclude(last_play__isnull=True).order_by('-last_play')
        # Get the paginator
        paginator = Paginator(musics, 16)
        more_musics = False
        try:
            page = int(request.data.get('page')) + 1

            musics = paginator.page(page)
            if(paginator.page(page).has_next()):
                more_musics = True
            else:
                more_musics = False
        except (InvalidPage, EmptyPage, ValueError):
            return HttpResponse("Error while refreshing the library, please reload the page", status=409)

        template = render_to_string("include/remote/library.html", {"musics": musics, "tab": "library-list-music", "more_musics": more_musics})
        data = {
            'template': template,
            'more_musics': more_musics
        }
        return JSONResponse(data)
    return HttpResponse(401)
