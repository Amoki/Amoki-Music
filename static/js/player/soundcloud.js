var iframeElement = document.getElementById('soundcloudPlayer');
var soundcloudPlayer = SC.Widget(iframeElement);
soundcloudPlayer.initialized = false;

soundcloudPlayer.bind(SC.Widget.Events.READY, function() {
  soundcloudPlayer.initialized = true;
});

var soundcloudPlayerControl = {
  play: function(options) {
    $(document).attr('title', options.name);
    soundcloudPlayer.load('https://api.soundcloud.com/tracks/' + options.musicId, function() {
      console.log(arguments)
      // Start time
      soundcloudPlayer.seekTo(options.timer_start * 1000 || 0);
      // End time
      soundcloudPlayer.unbind(SC.Widget.Events.PLAY_PROGRESS);
      soundcloudPlayer.bind(SC.Widget.Events.PLAY_PROGRESS, function(stats) {
        if(options.timer_end && stats.currentPosition >= options.timer_end * 1000) {
          soundcloud.pause();
        }
      });

      soundcloudPlayer.play();
    });
  },
  stop: function() {
    if(soundcloudPlayer.initialized ) {
      soundcloudPlayer.pause();
    }
  },
  volume_up: function() {
    if(soundcloudPlayer.initialized ) {
      soundcloudPlayer.setVolume(Math.min(soundcloudPlayer.getVolume() + 10, 100));
    }
  },
  volume_down: function() {
    if(soundcloudPlayer.initialized ) {
      soundcloudPlayer.setVolume(Math.max(soundcloudPlayer.getVolume() - 10, 0));
    }
  }
};
