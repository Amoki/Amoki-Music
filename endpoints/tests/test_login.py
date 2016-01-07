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

        response.status_code.should.be.eql(status.HTTP_401_UNAUTHORIZED)
        response.data.should.eql({'detail': 'Invalid credentials.'})

    # only test the case of a good credential check is done
    # the cases of wrong / malformed credentials is already heavily tested in test_utils.py
    def test_check_good_credentials(self):
        response = self.client.get('/check_credentials')

        response.status_code.should.be.eql(status.HTTP_200_OK)

        response.data.should.have.key('heartbeat')
        response.data.should.have.key('uri')
