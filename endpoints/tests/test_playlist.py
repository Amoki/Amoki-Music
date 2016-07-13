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

        self.mx = Music(
            music_id="x",
            name="x",
            thumbnail="https://x.com",
            total_duration=150,
            duration=104,
            url="https://www.x.com",
            source="soundcloud",
            timer_start=20,
            room=self.r,
        )
        self.mx.save()

        self.my = Music(
            music_id="y",
            name="y",
            thumbnail="https://y.com",
            total_duration=170,
            duration=104,
            url="https://www.y.com",
            source="soundcloud",
            timer_start=20,
            room=self.r,
        )
        self.my.save()

        self.pt = PlaylistTrack(track=self.m, room=self.r)
        self.pt.save()
        self.ptx = PlaylistTrack(track=self.mx, room=self.r, track_type=PlaylistTrack.SHUFFLE)
        self.ptx.save()
        self.pty = PlaylistTrack(track=self.my, room=self.r)
        self.pty.save()

    def test_get(self):
        response = self.client.get('/playlist')

        response.status_code.should.eql(status.HTTP_200_OK)

        list(self.r.playlist.all()).should.eql([self.pt, self.pty, self.ptx])

        expected_result = [
            {
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
                },
                'track_type': 0,
            },
            {
                'pk': self.pty.pk,
                'order': 1,
                'music': {
                    'pk': self.my.pk,
                    'music_id': 'y',
                    'name': 'y',
                    'thumbnail': 'https://y.com',
                    'total_duration': 170,
                    'duration': 104,
                    'url': 'https://www.y.com',
                    'source': 'soundcloud',
                    'timer_start': 20,
                    'count': 0,
                    'last_play': None,
                    'one_shot': False
                },
                'track_type': 0,
            },
            {
                'pk': self.ptx.pk,
                'order': 0,
                'music': {
                    'pk': self.mx.pk,
                    'music_id': 'x',
                    'name': 'x',
                    'thumbnail': 'https://x.com',
                    'total_duration': 150,
                    'duration': 104,
                    'url': 'https://www.x.com',
                    'source': 'soundcloud',
                    'timer_start': 20,
                    'count': 0,
                    'last_play': None,
                    'one_shot': False
                },
                'track_type': 1,
            }
        ]
        list(response.data).should.eql(expected_result)

    def test_delete(self):
        response = self.client.patch('/room', {'shuffle': True})
        self.r = self.reload(self.r)

        self.r.playlist.filter(track_type=PlaylistTrack.SHUFFLE).count().should.eql(1)
        response = self.client.delete('/playlist/%s' % self.ptx.pk)
        response.status_code.should.eql(status.HTTP_204_NO_CONTENT)

        self.r.playlist.filter(track_type=PlaylistTrack.SHUFFLE).count().should.eql(self.r.nb_shuffle_items)

    def test_delete_shuffle_playlistTrack(self):
        response = self.client.delete('/playlist/%s' % self.pt.pk)
        response.status_code.should.eql(status.HTTP_204_NO_CONTENT)

    def test_delete_unexisting(self):
        response = self.client.delete('/playlist/1337')
        response.status_code.should.eql(status.HTTP_404_NOT_FOUND)

    def test_post_bad_pk(self):
        response = self.client.post('/playlist/1894/top')

        response.status_code.should.eql(status.HTTP_404_NOT_FOUND)
        response.data.should.eql("Can't find this playlistTrack.")

    def test_post_bad_action(self):
        response = self.client.post('/playlist/%s/badaction' % self.pt.pk)

        response.status_code.should.eql(status.HTTP_400_BAD_REQUEST)
        response.data.should.eql('Action can only be: "%s"' % '" or "'.join(PlaylistTrack.ACTIONS))

        response = self.client.post('/playlist/%s/top/123456789' % self.pt.pk)
        # Should response 200 because top ignore the target (it don't need a target)
        response.status_code.should.eql(status.HTTP_200_OK)

    def test_post_above_and_below_action_without_target(self):
        response = self.client.post('/playlist/%s/above' % self.pt.pk)

        response.status_code.should.eql(status.HTTP_400_BAD_REQUEST)
        response.data.should.eql('"above" action needs a target parameter')

        response = self.client.post('/playlist/%s/below' % self.pt.pk)

        response.status_code.should.eql(status.HTTP_400_BAD_REQUEST)
        response.data.should.eql('"below" action needs a target parameter')

    def test_post_above_and_below_action_with_bad_target(self):
        response = self.client.post('/playlist/%s/above/1337' % self.pt.pk)

        response.status_code.should.eql(status.HTTP_404_NOT_FOUND)
        response.data.should.eql("Can't find this playlistTrack as target.")

        response = self.client.post('/playlist/%s/below/1337' % self.pt.pk)

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

        response = self.client.post('/playlist/%s/below/%s' % (self.pt.pk, pt2.pk))

        response.status_code.should.eql(status.HTTP_200_OK)
        list(self.r.playlist.all()).should.eql([self.pty, pt2, self.pt, self.ptx])

        response = self.client.post('/playlist/%s/above/%s' % (self.pt.pk, self.pty.pk))

        response.status_code.should.eql(status.HTTP_200_OK)
        list(self.r.playlist.all()).should.eql([self.pt, self.pty, pt2, self.ptx])

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
        
        # This test check the "order_with_respect" param too
        # self.ptx is a Shuffle track so it should always be AFTER the normal tracks !
        # (in fact it's not rly important because the system first check for Normal tracks then for Shuffle tracks
        #  but it's more a readability factor for the administration)
        response = self.client.post('/playlist/%s/bottom' % self.pt.pk)

        response.status_code.should.eql(status.HTTP_200_OK)
        list(self.r.playlist.all()).should.eql([self.pty, pt2, self.pt, self.ptx])

    def test_change_playlistTrack_type(self):
        response = self.client.post('/playlist/%s/changetype/SHUFFLE' % self.pt.pk)
        response.status_code.should.eql(status.HTTP_200_OK)
        
        self.pt = self.reload(self.pt)
        self.pt.track_type.should.eql(PlaylistTrack.SHUFFLE)

    def test_change_playlistTrack_type_bad_type(self):
        response = self.client.post('/playlist/%s/changetype/oui' % self.pt.pk)
        response.status_code.should.eql(status.HTTP_400_BAD_REQUEST)

        response = self.client.post('/playlist/%s/changetype' % self.pt.pk)
        response.status_code.should.eql(status.HTTP_400_BAD_REQUEST)
