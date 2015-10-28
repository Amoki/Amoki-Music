from utils.testcase import TestCase
from music.models import Music, PlaylistTrack
from music.serializers import MusicSerializer, PlaylistSerializer

import sure


class SerializersTestCase(TestCase):
    def test_music_serializer(self):
        m = Music(
            music_id='a',
            name='a',
            thumbnail='https://a.com',
            total_duration=114,
            url='https://www.a.com',
            source='youtube',
            room=self.r,
        )
        m.save()

        expected_serialization = {
            'pk': m.pk,
            'music_id': 'a',
            'name': 'a',
            'thumbnail': 'https://a.com',
            'total_duration': 114,
            'duration': 114,
            'url': 'https://www.a.com',
            'source': 'youtube',
            'timer_start': 0,
            'timer_end': None,
            'count': 0,
            'last_play': None
        }

        dict(MusicSerializer(m).data).should.eql(expected_serialization)

    def test_playlist_serializer(self):
        m = Music(
            music_id='a',
            name='a',
            thumbnail='https://a.com',
            total_duration=114,
            url='https://www.a.com',
            source='youtube',
            room=self.r,
        )
        m.save()

        pt = PlaylistTrack(track=m, room=self.r)
        pt.save()

        expected_serialization = {
            'pk': pt.pk,
            'order': 0,
            'music': {
                'pk': m.pk,
                'music_id': 'a',
                'name': 'a',
                'thumbnail': 'https://a.com',
                'total_duration': 114,
                'url': 'https://www.a.com',
                'source': 'youtube',
                'timer_start': 0,
                'timer_end': None,
                'count': 0,
                'last_play': None
            }
        }

        dict(PlaylistSerializer(pt).data).should.eql(expected_serialization)
