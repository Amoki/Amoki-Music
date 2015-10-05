from endpoints.tests.testcase import EndpointTestCase
from rest_framework import status


class TestRoom(EndpointTestCase):
    def test_enable_shuffle_on_empty_room(self):
        response = self.client.patch('/room', {'shuffle': True})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Can't activate shuffle when there is no musics.")
