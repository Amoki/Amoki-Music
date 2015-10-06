from endpoints.tests.testcase import EndpointTestCase
from rest_framework import status
from rest_framework.test import APIClient
from player.models import Room

import sure


class TestRooms(EndpointTestCase):
    def test_get(self):
        client = APIClient()
        response = client.get('/rooms')

        response.data.should.have.key('count')
        response.data.should.have.key('next')
        response.data.should.have.key('previous')
        response.data.should.have.key('results')
        response.data['results'].should.be.a(list)

        response.status_code.should.eql(status.HTTP_200_OK)

        self.assertResponseEqualsRoom(response.data['results'][0], Room.objects.all().first(), check_token=False)
