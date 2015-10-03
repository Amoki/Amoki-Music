from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from player.models import Room


class TestRoomEndpoint(TestCase):
    def reload(self, item):
        """
        Reload an item from DB
        """
        return item.__class__.objects.get(pk=item.pk)

    def setUp(self):
        self.r = Room(name="a", password="a")
        self.r.save()

    def test_enable_shuffle_on_empty_room(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.r.token)
        response = client.patch('/room', {'shuffle': True}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Can't activate shuffle when there is no musics.")
