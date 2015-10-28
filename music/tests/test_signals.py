from utils.testcase import TestCase
from music.models import Music

import sure


class TestTimer(TestCase):
    def test_update_duration_both_timer(self):
        music = Music(
            room=self.r,
            music_id="a",
            name="a",
            total_duration=211,
            thumbnail="https://a.com/a.jpg",
            timer_start=10,
            timer_end=62,
        )
        music.save()

        music.duration.should.eql(52)

    def test_update_duration_timer_start(self):
        music = Music(
            room=self.r,
            music_id="a",
            name="a",
            total_duration=203,
            thumbnail="https://a.com/a.jpg",
            timer_start=10,
            timer_end=None,
        )
        music.save()

        music.duration.should.eql(193)

    def test_update_duration_timer_end(self):
        music = Music(
            room=self.r,
            music_id="a",
            name="a",
            total_duration=220,
            thumbnail="https://a.com/a.jpg",
            timer_start=0,
            timer_end=55,
        )
        music.save()

        music.duration.should.eql(55)
