from utils.testcase import TestCase
from player.serializers import RoomSerializer, RoomsSerializer

import sure


class SerializersTestCase(TestCase):
    def test_room_serializer(self):
        expected_result = {
            'name': 'a',
            'current_music': None,
            'shuffle': False,
            'can_adjust_volume': False,
            'count_left': 0,
            'time_left': 0,
            'current_time_left': 0,
            'playlist': [],
            'volume': 10,
            'token': self.r.token,
            'current_time_past': 0,
            'current_time_past_percent': 0,
            'listeners': 0,
        }

        dict(RoomSerializer(self.r).data).should.eql(expected_result)

    def test_rooms_serializer(self):
        expected_result = {
            'name': 'a',
            'current_music': None,
            'shuffle': False,
            'can_adjust_volume': False,
            'count_left': 0,
            'time_left': 0,
            'current_time_left': 0,
            'playlist': [],
            'volume': 10,
            'listeners': 0,
        }

        dict(RoomsSerializer(self.r).data).should.eql(expected_result)
