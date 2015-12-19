var iframeElement = document.querySelector('iframe#soundcloudPlayer');
var iframeElementPreview = document.querySelector('iframe#soundcloudPreviewPlayer');
var soundcloudPlayer = SC.Widget(iframeElement);
var soundcloudPreviewPlayer = SC.Widget(iframeElementPreview);
soundcloudPlayer.initialized = false;
soundcloudPreviewPlayer.initialized = false;

soundcloudPlayer.bind(SC.Widget.Events.READY, function() {
  soundcloudPlayer.initialized = true;
  if(getCookie('playerOpen') && getCookie('playerOpen') === "true" && roomVM.room() && roomVM.room().currentMusic() && roomVM.room().currentMusic().source() === "soundcloud") {
    roomVM.openPlayer();
  }
});
soundcloudPreviewPlayer.bind(SC.Widget.Events.READY, function() {
  soundcloudPreviewPlayer.initialized = true;
});

soundcloudPlayer.bind(SC.Widget.Events.ERROR, function() {
  if($('iframe#soundcloudPlayer').is(":visible")) {
    console.error("Soundcloud error occured");
  }
});
soundcloudPreviewPlayer.bind(SC.Widget.Events.ERROR, function() {
  if($('iframe#soundcloudPreviewPlayer').is(":visible")) {
    console.error("Soundcloud error occured");
  }
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
          auto_play: true,
          callback: function() {
            soundcloudPlayer.setVolume(getCookie('volumePlayer') / 100);
            setTimeout(function() {
              soundcloudPlayer.seekTo(options.timer_start * 1000 || 0);
            }, 100);
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

var soundcloudPlayerPreviewControl = {
  play: function(options) {
    if(soundcloudPreviewPlayer.initialized) {
      soundcloudPreviewPlayer.load(
        'https://api.soundcloud.com/tracks/' + options.music_id,
        {
          buying: false,
          visual: true,
          hide_related: true,
        }
      );
    }
  },
  stop: function() {
    if(soundcloudPreviewPlayer.initialized) {
      soundcloudPreviewPlayer.pause();
    }
  },
  seekTo: function(options) {
    if(soundcloudPreviewPlayer.initialized) {
      soundcloudPreviewPlayer.seekTo(options.secondes * 1000);
    }
  },
  getState: function() {
    return 1;
  }
};
