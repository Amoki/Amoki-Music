var iframeElement = document.querySelector('iframe#soundcloudPlayer');
var soundcloudPlayer = SC.Widget(iframeElement);
soundcloudPlayer.current_volume;
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
      $('iframe#soundcloudPlayer').fadeIn(250);
      $( "#slider-vertical" ).fadeIn(250);
      soundcloudPlayer.load(
        'https://api.soundcloud.com/tracks/' + options.musicId,
        {
          buying: false,
          visual: true,
          hide_related: true,
          callback: function() {
            soundcloudPlayer.setVolume(cookie_volume/100);
            soundcloudPlayer.play();
            // Start time
            soundcloudPlayer.bind (SC.Widget.Events.PLAY,function(){
              soundcloudPlayer.seekTo(options.timer_start * 1000 || 0);
              soundcloudPlayer.unbind(SC.Widget.Events.PLAY);
            });
            // End time
            soundcloudPlayer.unbind(SC.Widget.Events.PLAY_PROGRESS);
            soundcloudPlayer.bind(SC.Widget.Events.PLAY_PROGRESS, function(stats) {
              if(options.timer_end && stats.currentPosition >= options.timer_end * 1000) {
                soundcloud.pause();
              }
            });
          },
        }
      );
    }
  },
  stop: function() {
    if(soundcloudPlayer.initialized ) {
      soundcloudPlayer.pause();
      $('#soundcloudPlayer').fadeOut(250);
      $( "#slider-vertical" ).fadeOut(250);
    }
  },
  volume_up: function() {
    if(soundcloudPlayer.initialized ) {
      soundcloudPlayer.getVolume(function(volume){
        soundcloudPlayer.setVolume(Math.min(volume + 0.1, 1));
      });
    }
  },
  volume_down: function() {
    if(soundcloudPlayer.initialized ) {
      soundcloudPlayer.getVolume(function(volume){
        soundcloudPlayer.setVolume(Math.max(volume - 0.1, 0));
      });
    }
  },
  set_volume: function(volume) {
    if (soundcloudPlayer.initialized ) {
      soundcloudPlayer.setVolume(volume/100);
    }
  },
};
