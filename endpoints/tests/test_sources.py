from endpoints.tests.testcase import EndpointTestCase
from rest_framework import status
from rest_framework.test import APIClient

import sure


class TestRooms(EndpointTestCase):
    def test_get(self):
        client = APIClient()
        response = client.get('/sources')

        response.status_code.should.eql(status.HTTP_200_OK)

        response.data.should.eql(['youtube', 'soundcloud'])
