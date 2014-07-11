import isodate
import urlparse


def get_youtube_id(url):
    url_data = urlparse.urlparse(url)
    query = urlparse.parse_qs(url_data.query)
    return query["v"][0]


def get_youtube_link(video_id):
    return "https://www.youtube.com/watch?v=" + video_id


def get_time_in_seconds(time):
    return isodate.parse_duration(time).total_seconds()
