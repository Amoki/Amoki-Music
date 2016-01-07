from utils.testcase import TestCase
from music.models import Music, PlaylistTrack
from player.models import Room, Events
from datetime import datetime, timedelta

import sure


class ModelsTestCase(TestCase):
    def test_reset_token(self):
        initial_token = self.r.token
        self.r.reset_token()

        self.r.token.should_not.eql(initial_token)

    def test_get_current_remaining_time(self):
        # Still no music
        self.r.get_current_remaining_time().should.eql(0)

        music = Music(
            room=self.r,
            music_id='a',
            name='a',
            total_duration=200,
            duration=200,
            thumbnail='https://a.com/a.jpg',
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
            music_id='a',
            name='a',
            total_duration=200,
            duration=200,
            thumbnail='https://a.com/a.jpg',
            last_play=datetime.now()
        )
        music.save()

        PlaylistTrack(track=music, room=self.r).save()

        self.r.get_remaining_time().should.eql(200)

    def test_get_current_time_past(self):
        self.r.get_current_time_past().should.eql(0)

        music = Music(
            room=self.r,
            music_id='a',
            name='a',
            total_duration=200,
            duration=200,
            thumbnail='https://a.com/a.jpg',
            last_play=datetime.now() - timedelta(minutes=2)  # Music started 2 minutes ago
        )
        music.save()

        self.r.current_music = music
        self.r.save()

        self.r.get_current_time_past().should.eql(120)

    def test_get_current_time_past_percent(self):
        self.r.get_current_time_past_percent().should.eql(0)

        music = Music(
            room=self.r,
            music_id='a',
            name='a',
            total_duration=240,
            duration=240,
            thumbnail='https://a.com/a.jpg',
            last_play=datetime.now() - timedelta(minutes=2)  # Music started 2 minutes ago
        )
        music.save()

        self.r.current_music = music
        self.r.save()

        self.r.get_current_time_past_percent().should.eql(float(50))

    def test_get_musics_remaining(self):
        music = Music(
            room=self.r,
            music_id='a',
            name='a',
            total_duration=200,
            duration=200,
            thumbnail='https://a.com/a.jpg',
        )
        music.save()

        PlaylistTrack(track=music, room=self.r).save()

        list(self.r.get_musics_remaining()).should.eql([music])

    def test_get_count_remaining(self):
        music = Music(
            room=self.r,
            music_id='a',
            name='a',
            total_duration=200,
            duration=200,
            thumbnail='https://a.com/a.jpg',
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

        self.r.volume.should.eql(95)

    def test_set_shuffle(self):
        self.r.set_shuffle.when.called_with(True).should.throw(Room.UnableToUpdate, "Can't activate shuffle when there is no musics.")

        music = Music(
            room=self.r,
            music_id='a',
            name='a',
            total_duration=200,
            duration=200,
            thumbnail='https://a.com/a.jpg',
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
            music_id='a',
            name='a',
            total_duration=200,
            duration=200,
            thumbnail='https://a.com/a.jpg',
            source='youtube'
        )
        music.save()

        self.r.update({'shuffle': True})

        self.r.shuffle.should.be.true

        self.r.update({'can_adjust_volume': True})

        self.r.can_adjust_volume.should.be.true

    def test_stop(self):
        music = Music(
            room=self.r,
            music_id='a',
            name='a',
            total_duration=200,
            duration=200,
            thumbnail='https://a.com/a.jpg',
        )
        music.save()

        self.r.current_music = music
        self.r.save()

        self.r.stop()

        self.r.current_music.should.be.none

    def test_play_next_without_shuffle(self):
        music = Music(
            room=self.r,
            music_id='a',
            name='a',
            total_duration=200,
            duration=200,
            thumbnail='https://a.com/a.jpg',
        )
        music.save()

        PlaylistTrack(track=music, room=self.r).save()

        self.r.play_next()

        self.r.current_music.should.eql(music)

        self.r.play_next()
        # No more music in the playlist.
        self.r.current_music.should.be.none

    def test_play_next_with_shuffle(self):
        music = Music(
            room=self.r,
            music_id='a',
            name='a',
            total_duration=200,
            duration=200,
            thumbnail='https://a.com/a.jpg',
        )
        music.save()

        music2 = Music(
            room=self.r,
            music_id='b',
            name='b',
            total_duration=200,
            duration=200,
            thumbnail='https://a.com/a.jpg',
        )
        music2.save()

        self.r.shuffle = True
        self.r.save()
        PlaylistTrack(track=music, room=self.r).save()

        self.r.play_next()
        self.r.current_music.should.eql(music)

        self.r.play_next()
        # No music in the playlist, but should select an other.
        self.r.current_music.should_not.be.none

    def test_add_music(self):
        music = Music(
            room=self.r,
            music_id='b',
            name='b',
            total_duration=200,
            duration=200,
            thumbnail='https://a.com/a.jpg',
            source='youtube'
        )
        music.save()

        self.r.add_music(music)
        self.r.music_set.count().should.eql(1)
        self.r.current_music.music_id.should.eql('b')

        self.r.add_music(music)

        self.r.tracks.count().should.eql(1)

    def test_play(self):
        music = Music(
            room=self.r,
            music_id='a',
            name='a',
            total_duration=200,
            duration=200,
            thumbnail='https://a.com/a.jpg',
        )
        music.save()

        self.r.play(music)

        self.r.current_music.should.eql(music)

        music.count.should.eql(1)
        music.last_play.should_not.be.none

        Events.get(self.r).should_not.be.none
