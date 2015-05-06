var iframeElement = document.querySelector('iframe#soundcloudPlayer');
var soundcloudPlayer = SC.Widget(iframeElement);
soundcloudPlayer.initialized = false;

soundcloudPlayer.bind(SC.Widget.Events.READY, function() {
  soundcloudPlayer.initialized = true;
  if(typeof current_music !== "undefined" && current_music_source === "Soundcloud"){
    soundcloudPlayerControl.play({
      musicId: current_music,
      timer_start: current_time_past
    });
  }
});

soundcloudPlayer.bind(SC.Widget.Events.ERROR, function(err) {
  console.error("Soundcloud error occured");
});

var soundcloudPlayerControl = {
  play: function(options) {
    if(soundcloudPlayer.initialized ) {
      $(document).attr('title', options.name);
      $('iframe#soundcloudPlayer').css("opacity", 1);
      console.log(options.timer_start);
      soundcloudPlayer.load(
        'https://api.soundcloud.com/tracks/' + options.musicId,
        {
          auto_play: true,
          buying: false,
        },
        function() {
          // Start time
          console.log(options.timer_start);
          soundcloudPlayer.seekTo(options.timer_start * 1000 || 0);
          // End time
          soundcloudPlayer.unbind(SC.Widget.Events.PLAY_PROGRESS);
          soundcloudPlayer.bind(SC.Widget.Events.PLAY_PROGRESS, function(stats) {
            if(options.timer_end && stats.currentPosition >= options.timer_end * 1000) {
              soundcloud.pause();
            }
          });
        }
      );
    }
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
