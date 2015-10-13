from utils.testcase import TestCase
from player.models import Events, Room

import sure


class TestSignals(TestCase):
    def test_update_token_on_password_change(self):
        first_token = self.r.token

        self.r.password = 'b'
        self.r.save()

        self.r.token.should_not.eql(first_token)

    def test_create_room_event(self):
        Room(name='b', password='b').save()

        Events.get_all().should.have.key('b')
