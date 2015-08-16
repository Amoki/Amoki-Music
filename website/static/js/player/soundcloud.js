var iframeElement = document.querySelector('iframe#soundcloudPlayer');
var soundcloudPlayer = SC.Widget(iframeElement);
soundcloudPlayer.currentVolume;
soundcloudPlayer.initialized = false;


var soundcloudPlayerControl = {
  play: function(options) {
    if(soundcloudPlayer.initialized) {
      $(document).attr('title', options.name);
      $('iframe#soundcloudPlayer').fadeIn(250);
      soundcloudPlayer.load(
        'https://api.soundcloud.com/tracks/' + options.musicId,
        {
          buying: false,
          visual: true,
          hide_related: true,
          callback: function() {
            soundcloudPlayer.setVolume(cookieVolume / 100);
            soundcloudPlayer.play();
            // Start time
            soundcloudPlayer.bind(SC.Widget.Events.PLAY, function() {
              soundcloudPlayer.seekTo(options.timerStart * 1000 || 0);
              soundcloudPlayer.unbind(SC.Widget.Events.PLAY);
            });
            // End time
            soundcloudPlayer.unbind(SC.Widget.Events.PLAY_PROGRESS);
            soundcloudPlayer.bind(SC.Widget.Events.PLAY_PROGRESS, function(stats) {
              if(options.timerEnd && stats.currentPosition >= options.timerEnd * 1000) {
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
      $('#soundcloudPlayer').fadeOut(250);
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


soundcloudPlayer.bind(SC.Widget.Events.READY, function() {
  soundcloudPlayer.initialized = true;
  if(typeof currentMsic !== "undefined" && currentMusicSource === "Soundcloud") {
    soundcloudPlayerControl.play({
      musicId: currentMusic,
      timerStart: currentTimePast
    });
  }
});

soundcloudPlayer.bind(SC.Widget.Events.ERROR, function() {
  console.error("Soundcloud error occured");
});
