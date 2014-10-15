# -*- coding: utf-8 -*-
import urlparse

from amoki_music.settings import YOUTUBE_KEY

from apiclient.discovery import build
from player.helpers.helpers import get_time_in_seconds

import json


youtube = build(
    "youtube",
    "v3",
    developerKey=YOUTUBE_KEY
)


def search(query):
    search_response = youtube.search().list(
        q=query,
        part="snippet",
        maxResults=4
    ).execute()

    videos = []

    for video in search_response.get("items", []):
        details = youtube.videos().list(
            part='contentDetails,statistics',
            id=video["id"]["videoId"],
        ).execute().get("items", [])[0]

        parsedVideo = {
            'id': video["id"]["videoId"],
            'title': video["snippet"]["title"],
            'description': video["snippet"]["description"],
            'thumbnail': video["snippet"]["thumbnails"]["default"],
            'views': details["statistics"]["viewCount"],
            'duration': get_time_in_seconds(details["contentDetails"]["duration"])
        }
        videos.append(parsedVideo)

    return videos


def get_id(url):
    url_data = urlparse.urlparse(url)
    query = urlparse.parse_qs(url_data.query)
    try:
        return query["v"][0]
    except:
        # The url is already an id
        return url


def get_link(video_id):
    return "https://www.youtube.com/watch?v=" + video_id
