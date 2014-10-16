# -*- coding: utf-8 -*-
from django.test import TestCase

from player.helpers import youtube


class testYoutube(TestCase):
	def test_api(this):
		youtube.search(u"libérée")
