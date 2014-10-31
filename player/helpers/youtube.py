# -*- coding: utf-8 -*-
import random
import string
from apiclient.discovery import build

from amoki_music.settings import YOUTUBE_KEY

from player.helpers.helpers import get_time_in_seconds
from player.models import TemporaryMusic


youtube = build(
    "youtube",
    "v3",
    developerKey=YOUTUBE_KEY
)


def get_info(ids):
    ids = ','.join(ids)
    details = youtube.videos().list(
        id=ids,
        part='snippet, contentDetails, statistics'
    ).execute()
    return details.get("items", [])


def search(query):
    requestId = ''.join(random.choice(string.lowercase) for i in range(64))

    search_response = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        maxResults=15
    ).execute()

    videos = []

    ids = []
    for video in search_response.get("items", []):
        ids.append(video["id"]["videoId"])

    for detail in get_info(ids):
        music = TemporaryMusic(
            url="https://www.youtube.com/watch?v=" + detail["id"],
            name=detail["snippet"]["title"],
            description=detail["snippet"]["description"][:200] + "...",
            thumbnail=detail["snippet"]["thumbnails"]["default"]["url"],
            views=detail["statistics"]["viewCount"],
            duration=get_time_in_seconds(detail["contentDetails"]["duration"]),
            requestId=requestId
        )
        videos.append(music)

    TemporaryMusic.objects.bulk_create(videos)

    return videos
