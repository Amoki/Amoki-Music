from utils.testcase import EndpointTestCase
from rest_framework import status
from rest_framework.test import APIClient

from django.utils.translation import ugettext_lazy as _

import sure


class TestUtils(EndpointTestCase):
    def test_fail_authentication(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'wrongToken')

        response = client.get('/room')

        response.status_code.should.eql(status.HTTP_401_UNAUTHORIZED)
        response.data.should.eql({'detail': _('Invalid token.')})

    def test_bad_formatted_authentication(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer')

        response = client.get('/room')

        response.status_code.should.eql(status.HTTP_401_UNAUTHORIZED)
        response.data.should.eql({'detail': _('Invalid token header. No credentials provided.')})

        client.credentials(HTTP_AUTHORIZATION='Bearer token1 token2')

        response = client.get('/room')

        response.status_code.should.eql(status.HTTP_401_UNAUTHORIZED)
        response.data.should.eql({'detail': _('Invalid token header. Token string should not contain spaces.')})

        client.credentials(HTTP_AUTHORIZATION='token')

        response = client.get('/room')

        response.status_code.should.eql(status.HTTP_401_UNAUTHORIZED)
        response.data.should.eql({'detail': _('Invalid token header. No credentials provided.')})
