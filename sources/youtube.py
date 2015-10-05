import re

from apiclient.discovery import build as youtube_api

from django.conf import settings

from utils.time import get_time_in_seconds

URL_REGEX = "(?:v=|youtu\.be\/)([^&?]+)"

youtube = youtube_api(
    "youtube",
    "v3",
    developerKey=settings.YOUTUBE_KEY
)


def get_info(ids):
    if not isinstance(ids, str):
        ids = ','.join(ids)
    details = youtube.videos().list(
        id=ids,
        part='snippet, contentDetails, statistics'
    ).execute()

    videos = []
    for detail in details.get("items", []):
        added = True
        if "regionRestriction" in detail["contentDetails"]:
            if "blocked" in detail["contentDetails"]["regionRestriction"]:
                if settings.YOUTUBE_LANGUAGE in detail["contentDetails"]["regionRestriction"]["blocked"]:
                    added = False
            if "allowed" in detail["contentDetails"]["regionRestriction"]:
                if len(detail["contentDetails"]["regionRestriction"]["allowed"]) == 0:
                    added = False
                else:
                    if settings.YOUTUBE_LANGUAGE not in detail["contentDetails"]["regionRestriction"]["allowed"]:
                        added = False

        if added:
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
            videoEmbeddable="true",
            regionCode="FR",
            relevanceLanguage="fr"
        ).execute()
        for video in search_response.get("items", []):
            ids.append(video["id"]["videoId"])
    else:
        # Get the id from url
        ids.append(regexVideoId.search(query).group(1))

    videos = []
    for video in get_info(ids):
        music = {
            "music_id": video['music_id'],
            "name": video['name'],
            "channel_name": video['channel_name'],
            "description": video['description'],
            "thumbnail": video['thumbnail'],
            "views": video['views'],
            "duration": video['duration'],
            "url": "https://www.youtube.com/watch?v=" + video['music_id'],
            "source": "youtube"
        }
        videos.append(music)

    return videos


def check_validity(id):
    detail = youtube.videos().list(
        id=id,
        part='contentDetails,status'
    ).execute()

    # General validity
    validity = True

    # Check if the video exist
    if detail["pageInfo"]["totalResults"] > 0:
        # Check if the music have a Country restriction
        country_validity = True
        if "regionRestriction" in detail["items"][0]["contentDetails"]:
            if "blocked" in detail["items"][0]["contentDetails"]["regionRestriction"]:
                if settings.YOUTUBE_LANGUAGE in detail["items"][0]["contentDetails"]["regionRestriction"]["blocked"]:
                    country_validity = False
            if "allowed" in detail["items"][0]["contentDetails"]["regionRestriction"]:
                if len(detail["items"][0]["contentDetails"]["regionRestriction"]["allowed"]) == 0:
                    country_validity = False
                else:
                    if settings.YOUTUBE_LANGUAGE not in detail["items"][0]["contentDetails"]["regionRestriction"]["allowed"]:
                        country_validity = False

        # Check if the music have an embeddable restriction
        embeddable_validity = True
        if not detail["items"][0]["status"]["embeddable"]:
            embeddable_validity = False

        if not country_validity or not embeddable_validity:
            validity = False
    else:
        validity = False

    return validity
