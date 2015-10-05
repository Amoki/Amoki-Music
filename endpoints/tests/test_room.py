from endpoints.tests.testcase import EndpointTestCase
from rest_framework import status
from rest_framework.test import APIClient

from player.models import Room
from music.models import Music, PlaylistTrack


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
            'token': self.r.token
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_result)

    def test_post(self):
        client = APIClient()
        response = client.post('/room', {'name': 'b', 'password': 'b'})

        room = Room.objects.get(name='b')
        expected_result = {
            'name': 'b',
            'current_music': None,
            'shuffle': False,
            'can_adjust_volume': False,
            'count_left': 0,
            'time_left': 0,
            'current_time_left': 0,
            'playlist': [],
            'volume': 10,
            'token': room.token
        }

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected_result)

    def test_patch_shuffle_while_empty_room(self):
        response = self.client.patch('/room', {'shuffle': True})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Can't activate shuffle when there is no musics.")

    def test_patch_shuffle(self):
        m = Music(
            music_id="a",
            name="a",
            thumbnail="https://a.com",
            duration=114,
            url="https://www.a.com",
            source="youtube",
            room=self.r,
        )
        m.save()

        response = self.client.patch('/room', {'shuffle': True})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['shuffle'])
        self.assertEqual(response.data['current_music']['music_id'], 'a')

        response = self.client.patch('/room', {'shuffle': False})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['shuffle'])

    def test_patch_can_adjust_volume(self):
        response = self.client.patch('/room', {'can_adjust_volume': True})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['can_adjust_volume'])

        response = self.client.patch('/room', {'can_adjust_volume': False})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['can_adjust_volume'])

    def test_patch_volume(self):
        self.client.patch('/room', {'can_adjust_volume': True})
        response = self.client.patch('/room', {'volume': 20})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['volume'], 20)

    def test_patch_volume_without_permission(self):
        self.client.patch('/room', {'can_adjust_volume': False})

        response = self.client.patch('/room', {'volume': 50})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "This room don't have permission to update volume.")

    def test_delete(self):
        response = self.client.delete('/room')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Room.objects.filter(name='a').exists())

    def test_next(self):
        m = Music(
            music_id="a",
            name="a",
            thumbnail="https://a.com",
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
            duration=114,
            url="https://www.a.com",
            source="youtube",
            room=self.r,
        )
        m2.save()
        PlaylistTrack.objects.create(room=self.r, track=m2)

        response = self.client.post('/room/next', {'music_pk': m.pk})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['current_music']['music_id'], m2.music_id)
