from utils.testcase import MusicTestCase
from player.models import events, Room


class TestSignals(MusicTestCase):
    def test_update_token_on_password_change(self):
        first_token = self.r.token

        self.r.password = 'b'
        self.r.save()

        self.assertNotEqual(self.reload(self.r).token, first_token)

    def test_create_room_event(self):
        Room(name='b', password='b').save()

        events.should.have.key('b')
