from utils.testcase import EndpointTestCase
from rest_framework import status
from rest_framework.test import APIClient

import sure


class TestLogin(EndpointTestCase):
    def test_login_successful(self):
        client = APIClient()
        response = client.get('/login', {'name': 'a', 'password': 'a'})

        response.status_code.should.eql(status.HTTP_200_OK)

        response.data.should.have.key('room')
        response.data.should.have.key('websocket')

        self.assertResponseEqualsRoom(response.data['room'], self.r)

    def test_login_fail_bad_params(self):
        client = APIClient()
        response = client.get('/login')

        response.status_code.should.be.eql(status.HTTP_400_BAD_REQUEST)
        response.data.should.be.eql("Missing name or password parameter")

    def test_login_fail_bad_credentials(self):
        client = APIClient()
        response = client.get('/login', {'name': 'a', 'password': 'b'})

        response.status_code.should.be.eql(status.HTTP_403_FORBIDDEN)
        response.data.should.eql({'detail': 'Invalid credentials.'})
