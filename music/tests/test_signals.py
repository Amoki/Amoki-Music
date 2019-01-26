from datetime import datetime
from utils.testcase import TestCase
from music.models import Events, Room, MusicQueue, Music


class TestRoomSignals(TestCase):
    def test_update_token_on_password_change(self):
        first_token = self.room.token

        self.room.password = "b"
        self.room.save()

        self.assertNotEqual(self.room.token, first_token)

    def test_create_room_event(self):
        Room(name="b", password="b").save()
        self.assertIsNotNone("b" in Events.get_all())


class TestMusicQueueSignals(TestCase):
    def test_music_queue_update_emit(self):
        music = Music.objects.create(
            room=self.room,
            music_id="a",
            name="a",
            total_duration=200,
            duration=200,
            thumbnail="https://a.com/a.jpg",
            last_play=datetime.now(),
            service="youtube",
        )
        self.room.shuffle = True
        self.room.save()
        self.room.play_next()
