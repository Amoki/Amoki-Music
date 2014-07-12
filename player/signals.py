# -*- coding: utf-8 -*-
from django.db.models.signals import pre_save
from django.dispatch import receiver
from amoki_music.settings import YOUTUBE_KEY
from player.models import Music
from player.helpers import get_time_in_seconds

import urllib2
import json


@receiver(pre_save, sender=Music)
def set_id_name_and_duration(sender, instance, **kwargs):
        query = "https://www.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails&id=" + instance.video_id + "&key=" + YOUTUBE_KEY
        body = urllib2.urlopen(query).read()
        res = json.loads(body)
        time = res["items"][0]["contentDetails"]["duration"]

        instance.duration = get_time_in_seconds(time)
        instance.name = res["items"][0]["snippet"]["title"]
        instance.thumbnail = res["items"][0]["snippet"]["thumbnails"]["default"]["url"]
