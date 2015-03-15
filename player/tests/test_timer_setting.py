# -*- coding: utf-8 -*-
from django.test import TestCase

from player.models import Room
from music.models import Music

# Music base: https://www.youtube.com/watch?v=E-p6l9nioNI
# Duration: 211
# Name: Mulan - Comme un homme
# Thumbnail: https://i.ytimg.com/vi/E-p6l9nioNI/default.jpg


class TestTimer(TestCase):

    def setUp(self):
        test_room = Room.objects.create(name="test", password="123")
        test_room.save()

    def test_update_duration_both_timer(self):
        test_room = Room.objects.get(name="test")
        test_room.push(
            music_id="E-p6l9nioNI",
            name="Mulan - Comme un homme",
            duration=211,
            thumbnail="https://i.ytimg.com/vi/E-p6l9nioNI/default.jpg",
            timer_start=10,
            timer_end=62,
        )
        music_added = Music.objects.get(music_id="E-p6l9nioNI")
        attempted_duration = (211 - 10 - (211 - 62))

        self.assertEqual(music_added.duration, attempted_duration)

    def test_update_duration_timer_start(self):
        test_room = Room.objects.get(name="test")
        test_room.push(
            music_id="3QAXFudxqRM",
            name="La Reine des Neiges - Je voudrais un bonhomme de neige",
            duration=203,
            thumbnail="https://i.ytimg.com/vi/3QAXFudxqRM/default.jpg",
            timer_start=10,
            timer_end=None,
        )
        music_added = Music.objects.get(music_id="3QAXFudxqRM")
        attempted_duration = (203 - 10)

        self.assertEqual(music_added.duration, attempted_duration)

    def test_update_duration_timer_end(self):
        test_room = Room.objects.get(name="test")
        test_room.push(
            music_id="wQP9XZc2Y_c",
            name="La Reine des Neiges - Libérée, délivrée",
            duration=220,
            thumbnail="https://i.ytimg.com/vi/wQP9XZc2Y_c/default.jpg",
            timer_start=0,
            timer_end=55,
        )
        music_added = Music.objects.get(music_id="wQP9XZc2Y_c")
        attempted_duration = (203 - (203 - 55))

        self.assertEqual(music_added.duration, attempted_duration)
