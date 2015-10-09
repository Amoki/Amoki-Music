var iframeElement = document.querySelector('iframe#soundcloudPlayer');
var soundcloudPlayer = SC.Widget(iframeElement);
soundcloudPlayer.initialized = false;

soundcloudPlayer.bind(SC.Widget.Events.READY, function() {
  soundcloudPlayer.initialized = true;
});

soundcloudPlayer.bind(SC.Widget.Events.ERROR, function() {
  console.error("Soundcloud error occured");
});

var soundcloudPlayerControl = {
  play: function(options) {
    if(soundcloudPlayer.initialized) {
      $('#wrapper-soundcloud-player').stop().fadeIn(250);
      soundcloudPlayer.load(
        'https://api.soundcloud.com/tracks/' + options.music_id,
        {
          buying: false,
          visual: true,
          hide_related: true,
          callback: function() {
            soundcloudPlayer.setVolume(Cookies.get('volumePlayer') / 100);
            soundcloudPlayer.play();
            // Start time
            soundcloudPlayer.bind(SC.Widget.Events.PLAY, function() {
              soundcloudPlayer.seekTo(options.timer_start * 1000 || 0);
              soundcloudPlayer.unbind(SC.Widget.Events.PLAY);
            });
            // End time
            soundcloudPlayer.unbind(SC.Widget.Events.PLAY_PROGRESS);
            soundcloudPlayer.bind(SC.Widget.Events.PLAY_PROGRESS, function(stats) {
              if(options.timer_end && stats.currentPosition >= options.timer_end * 1000) {
                soundcloudPlayer.pause();
              }
            });
          },
        }
        );
    }
  },
  stop: function() {
    if(soundcloudPlayer.initialized) {
      soundcloudPlayer.pause();
      $('#wrapper-soundcloud-player').stop().fadeOut(250);
    }
  },
  volumeUp: function() {
    if(soundcloudPlayer.initialized) {
      soundcloudPlayer.getVolume(function(volume) {
        soundcloudPlayer.setVolume(Math.min(volume + 0.1, 1));
      });
    }
  },
  volumeDown: function() {
    if(soundcloudPlayer.initialized) {
      soundcloudPlayer.getVolume(function(volume) {
        soundcloudPlayer.setVolume(Math.max(volume - 0.1, 0));
      });
    }
  },
  setVolume: function(volume) {
    if(soundcloudPlayer.initialized) {
      soundcloudPlayer.setVolume(volume / 100);
    }
  },
};



