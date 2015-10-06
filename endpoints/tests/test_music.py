from endpoints.tests.testcase import EndpointTestCase
from rest_framework import status
from rest_framework.test import APIClient

from player.models import Room
from music.models import Music, PlaylistTrack

import sure


class TestMusic(EndpointTestCase):
    def test_delete(self):
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

        response = self.client.delete('/music/' + str(m.pk))

        response.status_code.should.eql(status.HTTP_204_NO_CONTENT)

        Music.objects.filter(music_id="a", room=self.r).exists().should.be.false

    def test_delete_not_exists(self):
        response = self.client.delete('/music/42')

        response.status_code.should.eql(status.HTTP_404_NOT_FOUND)
