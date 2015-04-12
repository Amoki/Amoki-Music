# -*- coding: utf-8 -*-
import random
import string

import soundcloud

from amoki_music.settings.common import SOUNDCLOUD_KEY

from music.models import TemporaryMusic, Source

client = soundcloud.Client(client_id=SOUNDCLOUD_KEY)


class Soundcloud(Source):
    @staticmethod
    def search(query=None, ids=None):
        # see https://stackoverflow.com/questions/1132941/least-astonishment-in-python-the-mutable-default-argument
        if not ids:
            ids = []

        requestId = ''.join(random.choice(string.lowercase) for i in range(64))

        search_response = client.get('/tracks', q=query, ids=ids.join(','), limit=15)

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
