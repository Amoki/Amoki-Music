# -*- coding: utf-8 -*-
import random
import string
import isodate

from apiclient.discovery import build

from amoki_music.settings.common import YOUTUBE_KEY

from music.models import TemporaryMusic


youtube = build(
    "youtube",
    "v3",
    developerKey=YOUTUBE_KEY
)


def get_time_in_seconds(time):
    return isodate.parse_duration(time).total_seconds()


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


def search(query=None, ids=[]):
    requestId = ''.join(random.choice(string.lowercase) for i in range(64))

    if query:
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
            requestId=requestId,
        )
        videos.append(music)

    TemporaryMusic.objects.bulk_create(videos)

    return videos
