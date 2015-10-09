from utils.testcase import EndpointTestCase
from rest_framework import status
from rest_framework.test import APIClient

from django.utils.translation import ugettext_lazy as _


class TestUtils(EndpointTestCase):
    def test_fail_authentication(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'wrongToken')

        response = client.get('/room')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {'detail': _('Invalid token.')})

    def test_bad_formatted_authentication(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer')

        response = client.get('/room')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {'detail': _('Invalid token header. No credentials provided.')})

        client.credentials(HTTP_AUTHORIZATION='Bearer token1 token2')

        response = client.get('/room')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {'detail': _('Invalid token header. Token string should not contain spaces.')})

        client.credentials(HTTP_AUTHORIZATION='token')

        response = client.get('/room')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {'detail': _('Invalid token header. No credentials provided.')})

