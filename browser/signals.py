# -*- coding: utf-8 -*-
from django.db.models.signals import pre_save
from django.dispatch import receiver

from browser.models import Url
import urllib2
from BeautifulSoup import BeautifulSoup
import HTMLParser


@receiver(pre_save, sender=Url)
def set_name(sender, instance, **kwargs):
    soup = BeautifulSoup(urllib2.urlopen(instance.url))
    instance.name = HTMLParser.HTMLParser().unescape(soup.title.string)
