from utils.testcase import TestCase
from player.models import events, Room


class TestSignals(TestCase):
    def test_update_token_on_password_change(self):
        first_token = self.r.token

        self.r.password = 'b'
        self.r.save()

        self.assertNotEqual(self.r.token, first_token)

    def test_create_room_event(self):
        Room(name='b', password='b').save()

        events.should.have.key('b')
