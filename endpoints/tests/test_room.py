from utils.testcase import EndpointTestCase
from rest_framework import status
from rest_framework.test import APIClient

from player.models import Room
from music.models import Music, PlaylistTrack

import sure


class TestRoom(EndpointTestCase):
    def test_get(self):
        response = self.client.get('/room')

        expected_result = {
            'name': self.r.name,
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
            'listeners' : 0
        }

        response.status_code.should.eql(status.HTTP_200_OK)
        (dict(response.data)).should.eql(expected_result)

    def test_post(self):
        client = APIClient()
        response = client.post('/room', {'name': 'b', 'password': 'b'})

        room = Room.objects.get(name='b')

        response.status_code.should.eql(status.HTTP_201_CREATED)
        self.assertResponseEqualsRoom(response.data, room)

    def test_post_bad_arguments(self):
        client = APIClient()
        response = client.post('/room', {'name': 'b'})

        response.status_code.should.eql(status.HTTP_400_BAD_REQUEST)

    def test_patch_shuffle_while_empty_room(self):
        response = self.client.patch('/room', {'shuffle': True})
        response.status_code.should.eql(status.HTTP_400_BAD_REQUEST)
        response.data.should.eql("Can't activate shuffle when there is no musics.")

    def test_patch_shuffle(self):
        m = Music(
            music_id="a",
            name="a",
            thumbnail="https://a.com",
            total_duration=114,
            duration=114,
            url="https://www.a.com",
            source="youtube",
            room=self.r,
        )
        m.save()

        response = self.client.patch('/room', {'shuffle': True})

        response.status_code.should.eql(status.HTTP_200_OK)
        response.data['shuffle'].should.be.true
        response.data['current_music']['music_id'].should.eql('a')

        response = self.client.patch('/room', {'shuffle': False})

        response.status_code.should.eql(status.HTTP_200_OK)
        response.data['shuffle'].should.be.false

    def test_patch_can_adjust_volume(self):
        response = self.client.patch('/room', {'can_adjust_volume': True})

        response.status_code.should.eql(status.HTTP_200_OK)
        response.data['can_adjust_volume'].should.be.true

        response = self.client.patch('/room', {'can_adjust_volume': False})

        response.status_code.should.eql(status.HTTP_200_OK)
        response.data['can_adjust_volume'].should.be.false

    def test_patch_volume(self):
        self.client.patch('/room', {'can_adjust_volume': True})
        response = self.client.patch('/room', {'volume': 20})

        response.status_code.should.eql(status.HTTP_200_OK)
        response.data['volume'].should.eql(20)

    def test_patch_volume_without_permission(self):
        self.client.patch('/room', {'can_adjust_volume': False})

        response = self.client.patch('/room', {'volume': 50})

        response.status_code.should.eql(status.HTTP_400_BAD_REQUEST)
        response.data.should.eql("This room don't have permission to update volume.")

    def test_patch_bad_argument(self):
        self.client.patch('/room', {'can_adjust_volume': 'coucou'})

        response = self.client.patch('/room', {'volume': 50})

        response.status_code.should.eql(status.HTTP_400_BAD_REQUEST)

    def test_delete(self):
        response = self.client.delete('/room')
        response.status_code.should.eql(status.HTTP_204_NO_CONTENT)

        Room.objects.filter(name='a').exists().should.be.false

    def test_next(self):
        m = Music(
            music_id="a",
            name="a",
            thumbnail="https://a.com",
            total_duration=114,
            duration=114,
            url="https://www.a.com",
            source="youtube",
            room=self.r,
        )
        m.save()

        self.r.current_music = m
        self.r.save()

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
        PlaylistTrack.objects.create(room=self.r, track=m2)

        response = self.client.post('/room/next', {'music_pk': m.pk})

        response.status_code.should.eql(status.HTTP_200_OK)
        self.assertResponseEqualsMusic(response.data['current_music'], self.reload(m2))

    def test_next_bad_arguments(self):
        response = self.client.post('/room/next', {})

        response.status_code.should.eql(status.HTTP_400_BAD_REQUEST)
