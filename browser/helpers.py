import isodate
from urllib.parse import urlparse


def get_youtube_id(url):
    parsed = urlparse(url)
    print parsed
    if not "v=" in url:
        return url
    else:
        return url.rsplit("v=", 1)[1]


def get_youtube_link(video_id):
    return "https://www.youtube.com/watch?v=" + video_id


def get_time_in_seconds(time):
    return isodate.parse_duration(time).total_seconds()
