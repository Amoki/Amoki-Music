from utils.testcase import EndpointTestCase
from rest_framework import status

from music.models import Music, PlaylistTrack

import sure


class TestPlaylist(EndpointTestCase):
    def setUp(self):
        super().setUp()
        self.m = Music(
            music_id="a",
            name="a",
            thumbnail="https://a.com",
            total_duration=114,
            duration=104,
            url="https://www.a.com",
            source="youtube",
            timer_start=10,
            room=self.r,
        )
        self.m.save()

        self.pt = PlaylistTrack(track=self.m, room=self.r)
        self.pt.save()

    def test_get(self):
        response = self.client.get('/playlist')

        response.status_code.should.eql(status.HTTP_200_OK)

        expected_result = [{
            'pk': self.pt.pk,
            'order': 0,
            'music': {
                'pk': self.m.pk,
                'music_id': 'a',
                'name': 'a',
                'thumbnail': 'https://a.com',
                'total_duration': 114,
                'duration': 104,
                'url': 'https://www.a.com',
                'source': 'youtube',
                'timer_start': 10,
                'count': 0,
                'last_play': None,
                'one_shot': False
            }
        }]

        list(response.data).should.eql(expected_result)

    def test_delete(self):
        response = self.client.delete('/playlist', {'pk': self.pt.pk})
        response.status_code.should.eql(status.HTTP_204_NO_CONTENT)

    def test_delete_unexisting(self):
        response = self.client.delete('/playlist', {'pk': 9000})
        response.status_code.should.eql(status.HTTP_404_NOT_FOUND)

    def test_post_bad_pk(self):
        response = self.client.post('/playlist', {'pk': 9000, 'action': 'top'})

        response.status_code.should.eql(status.HTTP_404_NOT_FOUND)
        response.data.should.eql("Can't find this playlistTrack.")

    def test_post_bad_action(self):
        response = self.client.post('/playlist', {'pk': self.pt.pk, 'action': 'badaction'})

        response.status_code.should.eql(status.HTTP_400_BAD_REQUEST)
        response.data.should.eql('Action can only be: "%s"' % '" or "'.join(PlaylistTrack.ACTIONS))

    def test_post_above_and_below_action_without_target(self):
        response = self.client.post('/playlist', {'pk': self.pt.pk, 'action': 'above'})

        response.status_code.should.eql(status.HTTP_400_BAD_REQUEST)
        response.data.should.eql('"above" action needs a target parameter')

        response = self.client.post('/playlist', {'pk': self.pt.pk, 'action': 'below'})

        response.status_code.should.eql(status.HTTP_400_BAD_REQUEST)
        response.data.should.eql('"below" action needs a target parameter')

    def test_post_above_and_below_action_with_bad_target(self):
        response = self.client.post('/playlist', {'pk': self.pt.pk, 'action': 'above', 'target': 1337})

        response.status_code.should.eql(status.HTTP_404_NOT_FOUND)
        response.data.should.eql("Can't find this playlistTrack as target.")

        response = self.client.post('/playlist', {'pk': self.pt.pk, 'action': 'below', 'target': 1337})

        response.status_code.should.eql(status.HTTP_404_NOT_FOUND)
        response.data.should.eql("Can't find this playlistTrack as target.")

    def test_post_below_or_above_action(self):
        m2 = Music(
            music_id="b",
            name="b",
            thumbnail="https://a.com",
            total_duration=114,
            duration=114,
            url="https://www.a.com",
            source="youtube",
            room=self.r,
        )
        m2.save()

        pt2 = PlaylistTrack(track=m2, room=self.r)
        pt2.save()

        response = self.client.post('/playlist', {'pk': self.pt.pk, 'action': 'below', 'target': pt2.pk})

        response.status_code.should.eql(status.HTTP_200_OK)
        list(self.r.playlist.all()).should.eql([pt2, self.pt])

        response = self.client.post('/playlist', {'pk': pt2.pk, 'action': 'above', 'target': self.pt.pk})

        response.status_code.should.eql(status.HTTP_200_OK)
        list(self.r.playlist.all()).should.eql([pt2, self.pt])

    def test_other_action(self):
        m2 = Music(
            music_id="b",
            name="b",
            thumbnail="https://a.com",
            total_duration=114,
            duration=114,
            url="https://www.a.com",
            source="youtube",
            room=self.r,
        )
        m2.save()

        pt2 = PlaylistTrack(track=m2, room=self.r)
        pt2.save()

        # test only one action to test the endpoint. Actions themselves are already tested in OrderedModel lib

        response = self.client.post('/playlist', {'pk': pt2.pk, 'action': 'top'})

        response.status_code.should.eql(status.HTTP_200_OK)
        list(self.r.playlist.all()).should.eql([pt2, self.pt])
