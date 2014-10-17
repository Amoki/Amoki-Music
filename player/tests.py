# -*- coding: utf-8 -*-
from django.test import TestCase

from player.helpers import youtube
from player.models import TemporaryMusic


class testYoutube(TestCase):
	def test_api(self):
		requestId = youtube.search(u"libérée")
		self.assertEqual(TemporaryMusic.objects.filter(requestId=requestId).count(), 15)

		TemporaryMusic.clean(requestId)

		self.assertEqual(TemporaryMusic.objects.filter(requestId=requestId).count(), 0)
