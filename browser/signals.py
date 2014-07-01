# -*- coding: utf-8 -*-
from django.db.models.signals import pre_save
from django.dispatch import receiver

from browser.models import Url
import urllib2
from BeautifulSoup import BeautifulSoup
import HTMLParser
import json


@receiver(pre_save, sender=Url)
def set_name(sender, instance, **kwargs):
    soup = BeautifulSoup(urllib2.urlopen(instance.url))
    instance.name = HTMLParser.HTMLParser().unescape(soup.title.string)


@receiver(pre_save, sender=Url)
def set_duration(sender, instance, **kwargs):
    try:
        video_id = instance.url.rsplit("v=", 1)[1]
        query = "https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id=" + video_id + "&key=AIzaSyAFstaFPAwbEb46OCCawakLha7B7qA5mo4"
        body = urllib2.urlopen(query).read()
        res = json.loads(body)
        raw_time = res["items"][0]["contentDetails"]["duration"]

        time = int(raw_time.rsplit("M", 1)[1].rsplit("S", 1)[0])
        time += 60 * int(raw_time.rsplit("M", 1)[0].rsplit("T", 1)[1])

        instance.duration = time
    except:
        instance.time = 5
