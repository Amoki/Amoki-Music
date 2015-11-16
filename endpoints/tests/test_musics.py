from utils.testcase import EndpointTestCase
from rest_framework import status
from music.models import Music
from player.models import Room

import sure


class TestMusics(EndpointTestCase):
    def test_get(self):
        m = Music(
            music_id="a",
            name="a",
            thumbnail="https://a.com",
            total_duration=114,
            duration=114,
            url="https://www.a.com",
            source="youtube",
            room=self.r,
        )
        m.save()

        # Create new room and a new music that should not be sent by /musics
        r2 = Room(name='b', password='b')
        r2.save()
        Music(
            music_id="a",
            name="a",
            thumbnail="https://a.com",
            total_duration=114,
            duration=114,
            url="https://www.a.com",
            source="youtube",
            room=r2,
        ).save()

        response = self.client.get('/musics')

        response.status_code.should.eql(status.HTTP_200_OK)

        response.data.should.have.key('count')
        response.data.should.have.key('next')
        response.data.should.have.key('previous')
        response.data.should.have.key('results')
        response.data['results'].should.be.a(list)
        response.data['results'].should.have.length_of(1)

        self.assertResponseEqualsMusic(response.data['results'][0], Music.objects.all().first())
