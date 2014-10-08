# -*- coding: utf-8 -*-

import isodate
import urlparse
import subprocess
from amoki_music.settings import PROJECT_ROOT
import platform
import os


def get_youtube_id(url):
    url_data = urlparse.urlparse(url)
    query = urlparse.parse_qs(url_data.query)
    try:
        return query["v"][0]
    except:
        # The url is already an id
        return url


def get_youtube_link(video_id):
    return "https://www.youtube.com/watch?v=" + video_id


def get_time_in_seconds(time):
    return isodate.parse_duration(time).total_seconds()


def increase_volume():
    if platform.system() == "Windows":
        print(PROJECT_ROOT + '\\utils\\nircmd.exe changesysvolume 4000')
        os.system(PROJECT_ROOT + '\\utils\\nircmd.exe changesysvolume 4000')


def decrease_volume():
    if platform.system() == "Windows":
        print(PROJECT_ROOT + '\\utils\\nircmd.exe changesysvolume -4000')
        os.system(PROJECT_ROOT + '\\utils\\nircmd.exe changesysvolume -4000')
