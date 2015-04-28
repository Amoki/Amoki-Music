# -*- coding: utf-8 -*-

import random
import string
import re
import soundcloud
import json

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
            raw_response = client.get('/tracks', q=query, limit=15)

            # Sometimes soundcloud send us a result like: [music1, music2]
            # sometimes, it: {"collection": [music1, music2]}
            # In the second case, the lib crash. So we parse ourselves the response
            response = json.loads(raw_response.raw_data)
            if 'collection' in response:
                response = response['collection']
        else:
            # Get the id from url
            raw_response = client.get('/resolve.json', url=query)
            response = json.loads(raw_response.raw_data)

        requestId = ''.join(random.choice(string.lowercase) for i in range(64))

        soundcloud = Source.objects.get(name="Soundcloud")
        videos = []
        for video in response:
            music = TemporaryMusic(
                music_id=video['id'],
                name=video['title'],
                channel_name=video['user']['username'],
                description=video['description'][:200] + "..." if video['description'] else '',
                thumbnail=video['artwork_url'] if video['artwork_url'] else "http://" + settings.SITE_URL + "/static/img/soundcloud-100x100.jpg",
                views=video['playback_count'],
                duration=int(video['duration'] / 1000),
                url=video['permalink_url'],
                requestId=requestId,
                source=soundcloud
            )
            videos.append(music)

        TemporaryMusic.objects.bulk_create(videos)

        return videos
