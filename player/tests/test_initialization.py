from django.conf import settings
from utils.testcase import TestCase
from player.models import Room, Events
from music.models import Music

from player.initialization import Init

import sure


class InitilizationTestCase(TestCase):
    def test_initialization(self):
        settings.TESTING = False

        # Create fake app to test "ready" method
        init = Init.create('player')
        init.models = {
            'room': Room
        }

        # Clean events
        Events.events = {}
        Events.get_all().should_not.have.key('a')  # Sanity check of events have been cleared

        room = Room(password='b', name='b')
        room.save()

        music = Music(
            room=room,
            music_id="a",
            name="a",
            total_duration=211,
            thumbnail="https://a.com/a.jpg",
        )
        music.save()

        room.current_music = music
        room.shuffle = True
        room.save()

        init.ready()

        room = self.reload(room)
        room.current_music.should.be.none
        room.shuffle.should.be.false
        Events.get_all().should.have.key('b')
        Events.get_all().should.have.key('a')

        settings.TESTING = True
