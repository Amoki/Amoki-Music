# -*- coding: utf-8 -*-
from django.db.models.signals import pre_save
from django.dispatch import receiver

from browser.models import Music

import urllib2
import json


@receiver(pre_save, sender=Music)
def set_id_name_and_duration(sender, instance, **kwargs):
    video_id = instance.video_id
    query = "https://www.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails&id=" + video_id + "&key=AIzaSyCt5t3qv1MTXW5Vaq0KB9__0m7xP5bQNo4"
    body = urllib2.urlopen(query).read()
    res = json.loads(body)
    raw_time = res["items"][0]["contentDetails"]["duration"]
    time = int(raw_time.rsplit("M", 1)[1].rsplit("S", 1)[0])
    time += 60 * int(raw_time.rsplit("M", 1)[0].rsplit("PT", 1)[1])
    # TODO : handle hours
    instance.duration = time
    instance.video_id = video_id
    instance.name = res["items"][0]["snippet"]["title"]
