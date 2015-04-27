# -*- coding: utf-8 -*-

import random
import string
import re
import soundcloud

from django.conf import settings


from music.models import TemporaryMusic, Source

client = soundcloud.Client(client_id=settings.SOUNDCLOUD_KEY)

URL_REGEX = "^https?:\/\/(soundcloud.com|snd.sc)\/(.*)$"


class Soundcloud(Source):
    @staticmethod
    def search(query):
        regexVideoId = re.compile(URL_REGEX, re.IGNORECASE | re.MULTILINE)
        if regexVideoId.search(query) is None:
            # The query is not an url
            search_response = client.get('/tracks', q=query, limit=15)
        else:
            # Get the id from url
            search_response = client.get('/resolve.json', url=query)

        requestId = ''.join(random.choice(string.lowercase) for i in range(64))

        soundcloud = Source.objects.get(name="Soundcloud")
        videos = []
        for video in search_response:
            music = TemporaryMusic(
                music_id=video.id,
                name=video.title,
                channel_name=video.user['username'],
                description=unicode(video.description)[:200] + "...",
                thumbnail=video.artwork_url if video.artwork_url else "http://" + settings.SITE_URL + "/static/img/soundcloud-100x100.jpg",
                views=video.playback_count,
                duration=int(video.duration / 1000),
                url=video.permalink_url,
                requestId=requestId,
                source=soundcloud
            )
            videos.append(music)

        TemporaryMusic.objects.bulk_create(videos)

        return videos
