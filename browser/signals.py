# -*- coding: utf-8 -*-
from django.db.models.signals import pre_save
from django.dispatch import receiver

from browser.models import Music

import urllib
import json


def get_youtube_id(url):
    if not "v=" in url:
        return url
    else:
        return url.rsplit("v=", 1)[1]


def get_youtube_link(id):
    return "https://www.youtube.com/watch?v=" + id


@receiver(pre_save, sender=Music)
def set_url_name_and_duration(sender, instance, **kwargs):
    video_id = get_youtube_id(instance.url)
    query = "https://www.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails&id=" + video_id + "&key=AIzaSyCt5t3qv1MTXW5Vaq0KB9__0m7xP5bQNo4"
    body = urllib.request.urlopen(query).read()
    res = json.loads(body.decode())

    raw_time = res["items"][0]["contentDetails"]["duration"]
    time = int(raw_time.rsplit("M", 1)[1].rsplit("S", 1)[0])
    time += 60 * int(raw_time.rsplit("M", 1)[0].rsplit("PT", 1)[1])
    # TODO : handle hours
    instance.duration = time
    instance.url = get_youtube_link(video_id)
    instance.name = res["items"][0]["snippet"]["title"]
