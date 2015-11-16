from utils.testcase import EndpointTestCase
from rest_framework import status

from music.models import Music
from player.models import Events

import sure


class TestMusic(EndpointTestCase):
    def test_delete(self):
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

        response = self.client.delete('/music/%s' % m.pk)

        response.status_code.should.eql(status.HTTP_204_NO_CONTENT)

        Music.objects.filter(music_id="a", room=self.r).exists().should.be.false

    def test_delete_current_music(self):
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
        self.r.current_music = m
        self.r.save()

        response = self.client.delete('/music/%s' % m.pk)

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
            total_duration=114,
            duration=114,
            url="https://www.a.com",
            source="youtube",
            room=self.r,
        )
        m.save()

        response = self.client.patch('/music/%s' % m.pk, {'timer_start': 8, 'duration': 106})

        response.status_code.should.eql(status.HTTP_200_OK)

        m = self.reload(m)

        m.timer_start.should.eql(8)
        m.duration.should.eql(106)

    def test_post_or_patch_current_music(self):
        music_to_post = {
            "music_id": "a",
            "name": "a",
            "thumbnail": "https://a.com",
            "total_duration": 114,
            "duration": 114,
            "url": "https://www.a.com",
            "source": "youtube",
        }
        self.client.post('/music', music_to_post)
        self.r = self.reload(self.r)
        firstEvent = Events.get(self.r)

        m = self.r.current_music
        self.client.patch('/music/%s' % m.pk, {'duration': 100})

        # Can't check more precisely the event because of the variable time for the script to execute
        # We at least check if the event is different so we can deduce that it has been updated
        secondEvent = Events.get(self.reload(self.r))
        secondEvent.shouldnt.eql(firstEvent)

        self.client.post('/music', music_to_post)
        self.r = self.reload(self.r)
        lastEvent = Events.get(self.r)

        lastEvent.shouldnt.eql(secondEvent)

    def test_patch_unexisting_music(self):
        response = self.client.patch('/music/165423123', {'timer_start': 8})

        response.status_code.should.eql(status.HTTP_404_NOT_FOUND)

    def test_patch_bad_arguments(self):
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

        response = self.client.patch('/music/%s' % m.pk, {'total_duration': 'wtf'})

        response.status_code.should.eql(status.HTTP_400_BAD_REQUEST)

    def test_post(self):
        music_to_post = {
            "music_id": "a",
            "name": "a",
            "thumbnail": "https://a.com",
            "total_duration": 114,
            "duration": 114,
            "url": "https://www.a.com",
            "source": "youtube",
        }

        response = self.client.post('/music', music_to_post)

        response.status_code.should.eql(status.HTTP_201_CREATED)

        Music.objects.filter(music_id='a', room=self.r).exists().should.be.true

    def test_post_existing_music(self):
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

        music_to_post = {
            "music_id": "a",
            "name": "a",
            "thumbnail": "https://a.com",
            "total_duration": 114,
            "duration": 100,
            "url": "https://www.a.com",
            "source": "youtube",
        }

        response = self.client.post('/music', music_to_post)

        response.status_code.should.eql(status.HTTP_201_CREATED)

        Music.objects.filter(music_id='a', room=self.r).first().duration.should.be.eql(100)

    def test_post_bad_arguments(self):
        music_to_post = {
            "music_id": "a"
        }

        response = self.client.post('/music', music_to_post)

        response.status_code.should.eql(status.HTTP_400_BAD_REQUEST)
