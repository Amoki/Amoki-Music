from utils.testcase import EndpointTestCase
from rest_framework import status

from music.models import Music

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

    def test_delete_current_music(self):
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
        self.r.current_music = m
        self.r.save()

        response = self.client.delete('/music/' + str(m.pk))

        response.status_code.should.eql(status.HTTP_204_NO_CONTENT)

        Music.objects.filter(music_id="a", room=self.r).exists().should.be.false

    def test_delete_not_exists(self):
        response = self.client.delete('/music/42')

        response.status_code.should.eql(status.HTTP_404_NOT_FOUND)

    def test_patch(self):
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

        response = self.client.patch('/music/' + str(m.pk), {'timer_start': 8, "timer_end": 100})

        response.status_code.should.eql(status.HTTP_200_OK)

        m = self.reload(m)

        m.timer_start.should.eql(8)
        m.timer_end.should.eql(100)
        m.duration.should.eql(92)

    def test_patch_unexisting_music(self):
        response = self.client.patch('/music/165423123', {'timer_start': 8, "timer_end": 100})

        response.status_code.should.eql(status.HTTP_404_NOT_FOUND)

    def test_patch_bad_arguments(self):
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

        response = self.client.patch('/music/' + str(m.pk), {'duration': 'wtf'})

        response.status_code.should.eql(status.HTTP_400_BAD_REQUEST)

    def test_post(self):
        music_to_post = {
            "music_id": "a",
            "name": "a",
            "thumbnail": "https://a.com",
            "duration": 114,
            "url": "https://www.a.com",
            "source": "youtube",
        }

        response = self.client.post('/music', music_to_post)

        response.status_code.should.eql(status.HTTP_201_CREATED)

        Music.objects.filter(music_id='a', room=self.r).exists().should.be.true

    def test_post_bad_arguments(self):
        music_to_post = {
            "music_id": "a"
        }

        response = self.client.post('/music', music_to_post)

        response.status_code.should.eql(status.HTTP_400_BAD_REQUEST)
