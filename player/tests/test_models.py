from utils.testcase import MusicTestCase
from music.models import Music, PlaylistTrack
from player.models import Room
from datetime import datetime, timedelta

import sure


class ModelsTestCase(MusicTestCase):
    def test_reset_token(self):
        initial_token = self.r.token
        self.r.reset_token()

        self.r.token.should_not.eql(initial_token)

    def test_get_current_remaining_time(self):
        # Still no music
        self.r.get_current_remaining_time().should.eql(0)

        music = Music(
            room=self.r,
            music_id="a",
            name="a",
            duration=200,
            thumbnail="https://a.com/a.jpg",
            last_play=datetime.now()
        )
        music.save()

        self.r.current_music = music
        self.r.save()

        self.r.get_current_remaining_time().should.eql(200)

    def test_get_remaining_time(self):
        # Still no music
        self.r.get_remaining_time().should.eql(0)

        music = Music(
            room=self.r,
            music_id="a",
            name="a",
            duration=200,
            thumbnail="https://a.com/a.jpg",
            last_play=datetime.now()
        )
        music.save()

        PlaylistTrack(track=music, room=self.r).save()

        self.r.get_remaining_time().should.eql(200)

    def test_get_current_time_past(self):
        music = Music(
            room=self.r,
            music_id="a",
            name="a",
            duration=200,
            thumbnail="https://a.com/a.jpg",
            last_play=datetime.now() - timedelta(minutes=2)  # Music started 2 minutes ago
        )
        music.save()

        self.r.current_music = music
        self.r.save()

        self.r.get_current_time_past().should.eql(120)

    def test_get_current_time_past_percent(self):
        music = Music(
            room=self.r,
            music_id="a",
            name="a",
            duration=240,
            thumbnail="https://a.com/a.jpg",
            last_play=datetime.now() - timedelta(minutes=2)  # Music started 2 minutes ago
        )
        music.save()

        self.r.current_music = music
        self.r.save()

        self.r.get_current_time_past_percent().should.eql(float(50))

    def test_get_musics_remaining(self):
        music = Music(
            room=self.r,
            music_id="a",
            name="a",
            duration=200,
            thumbnail="https://a.com/a.jpg",
            last_play=datetime.now()
        )
        music.save()

        PlaylistTrack(track=music, room=self.r).save()

        list(self.r.get_musics_remaining()).should.eql([music])

    def test_get_count_remaining(self):
        music = Music(
            room=self.r,
            music_id="a",
            name="a",
            duration=200,
            thumbnail="https://a.com/a.jpg",
            last_play=datetime.now()
        )
        music.save()

        PlaylistTrack(track=music, room=self.r).save()

        self.r.get_count_remaining().should.eql(1)

    def test_set_volume(self):
        self.r.can_adjust_volume = False
        self.r.save()

        self.r.set_volume.when.called_with(10).should.throw(Room.UnableToUpdate, "This room don't have permission to update volume.")

        self.r.can_adjust_volume = True
        self.r.save()

        self.r.set_volume(95)

        self.reload(self.r).volume.should.eql(95)

    def test_set_shuffle(self):
        self.r.set_shuffle.when.called_with(True).should.throw(Room.UnableToUpdate, "Can't activate shuffle when there is no musics.")

        music = Music(
            room=self.r,
            music_id="a",
            name="a",
            duration=200,
            thumbnail="https://a.com/a.jpg",
            last_play=datetime.now()
        )
        music.save()

        self.r.set_shuffle(True)

        self.r.shuffle.should.be.true
        self.r.current_music.should.eql(music)

        self.r.set_shuffle(False)
        self.r.shuffle.should.be.false

    def test_update(self):
        music = Music(
            room=self.r,
            music_id="a",
            name="a",
            duration=200,
            thumbnail="https://a.com/a.jpg",
            last_play=datetime.now()
        )
        music.save()

        self.r.update({'shuffle': True})

        self.r.shuffle.should.be.true

        self.r.update({'can_adjust_volume': True})

        self.r.can_adjust_volume.should.be.true


"""
def update(self, modifications):
        for key, value in modifications.items():
            if key in setters['with_setters']:
                getattr(self, 'set_%s' % key)(value)
            elif key in setters['without_setters']:
                setattr(self, key, value)
                self.save()
                """
