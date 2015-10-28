from django.conf import settings
from utils.testcase import TestCase
from music.models import Music, PlaylistTrack

from music.initialization import Init

import sure


class InitilizationTestCase(TestCase):
    def test_initialization(self):
        settings.TESTING = False

        # Create fake app to test ready method
        init = Init.create('music')
        init.models = {
            'playlisttrack': PlaylistTrack
        }

        music = Music(
            room=self.r,
            music_id="a",
            name="a",
            total_duration=211,
            thumbnail="https://a.com/a.jpg",
        )
        music.save()

        PlaylistTrack(track=music, room=self.r).save()

        init.ready()

        self.r.tracks.count().should.eql(0)

        settings.TESTING = True
