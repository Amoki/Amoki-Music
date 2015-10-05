from endpoints.tests.testcase import EndpointTestCase
from rest_framework import status
from rest_framework.test import APIClient


class TestLogin(EndpointTestCase):
    def test_login_successful(self):
        client = APIClient()
        response = client.get('/login', {'name': 'a', 'password': 'a'})

        expected_response = {
            'room': {
                'name': self.r.name,
                'current_music': None,
                'shuffle': False,
                'can_adjust_volume': False,
                'count_left': 0,
                'time_left': 0,
                'current_time_left': 0,
                'playlist': [],
                'token': self.r.token
            },
            'websocket': {
                'heartbeat': '--heartbeat--',
                'uri': 'ws://testserver/ws/'
            }
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('room', response.data)
        self.assertIn('websocket', response.data)
        self.assertEqual(self.r.token, response.data['room']['token'])

        self.assertEqual(response.data, expected_response)

    def test_login_fail_bad_params(self):
        client = APIClient()
        response = client.get('/login')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Missing name or password parameter")

    def test_login_fail_bad_credentials(self):
        client = APIClient()
        response = client.get('/login', {'name': 'a', 'password': 'b'})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {'detail': 'Invalid credentials.'})
