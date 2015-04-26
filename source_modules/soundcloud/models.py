# -*- coding: utf-8 -*-
import random
import string
import re

import soundcloud

from amoki_music.settings.common import SOUNDCLOUD_KEY

from music.models import TemporaryMusic, Source

client = soundcloud.Client(client_id=SOUNDCLOUD_KEY)

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

        videos = []
        for video in search_response:
            music = TemporaryMusic(
                music_id=video['id'],
                name=video['title'],
                channel_name=video['user']['username'],
                description=video['description'][:200] + "...",
                thumbnail=video['artwork_url'],
                views=video['playback_count'],
                duration=video['duration'] / 1000,
                requestId=requestId,
            )
            videos.append(music)

        TemporaryMusic.objects.bulk_create(videos)

        return videos
