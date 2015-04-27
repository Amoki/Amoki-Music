# -*- coding: utf-8 -*-
import random
import string
import re

from apiclient.discovery import build as youtube_api

from amoki_music.settings.common import YOUTUBE_KEY

from music.models import TemporaryMusic, Source
from utils.time import get_time_in_seconds

URL_REGEX = "(?:v=|youtu\.be\/)([^&?]+)"

youtube = youtube_api(
    "youtube",
    "v3",
    developerKey=YOUTUBE_KEY
)


def get_info(ids):
    if type(ids) is not unicode:
        ids = ','.join(ids)
    details = youtube.videos().list(
        id=ids,
        part='snippet, contentDetails, statistics'
    ).execute()

    videos = []

    for detail in details.get("items", []):
        detailedVideo = {
            'music_id': detail["id"],
            'name': detail["snippet"]["title"],
            'channel_name': detail["snippet"]["channelTitle"],
            'description': detail["snippet"]["description"][:200] + "...",
            'thumbnail': detail["snippet"]["thumbnails"]["default"]["url"],
            'views': detail["statistics"]["viewCount"],
            'duration': get_time_in_seconds(detail["contentDetails"]["duration"]),
        }
        videos.append(detailedVideo)

    return videos


class Youtube(Source):
    @staticmethod
    def search(query):
        ids = []

        regexVideoId = re.compile(URL_REGEX, re.IGNORECASE | re.MULTILINE)
        if regexVideoId.search(query) is None:
            # The query is not an url
            search_response = youtube.search().list(
                q=query,
                part="id",
                type="video",
                maxResults=15,
                videoSyndicated="true",
                regionCode="FR",
                relevanceLanguage="fr"
            ).execute()
            for video in search_response.get("items", []):
                ids.append(video["id"]["videoId"])
        else:
            # Get the id from url
            ids.append(regexVideoId.search(query).group(1))

        requestId = ''.join(random.choice(string.lowercase) for i in range(64))
        youtube_source = Source.objects.get(name="Youtube")

        videos = []
        for video in get_info(ids):
            music = TemporaryMusic(
                music_id=video['music_id'],
                name=video['name'],
                channel_name=video['channel_name'],
                description=video['description'],
                thumbnail=video['thumbnail'],
                views=video['views'],
                duration=video['duration'],
                url="https://www.youtube.com/watch?v=" + video['music_id'],
                requestId=requestId,
                source=youtube_source
            )
            videos.append(music)

        TemporaryMusic.objects.bulk_create(videos)

        return videos
