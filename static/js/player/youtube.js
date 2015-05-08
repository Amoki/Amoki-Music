// Youtube iframe init
var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

// This function creates an <iframe> (and YouTube player)
// after the API code downloads.
function onYouTubeIframeAPIReady() {
  youtubePlayer = new YT.Player('youtubePlayer', {
    height: '390',
    width: '640',
    playerVars: {iv_load_policy: '3',modestbranding:'1',rel:'0',controls:'0',},
    events: {
      onReady : function(){
        youtubePlayer.initialized = true;
        $( "#slider-vertical" ).slider("value", youtubePlayerControl.get_volume());
        if(typeof current_music !== "undefined" && current_music_source === "Youtube"){
          youtubePlayerControl.play({
            musicId: current_music,
            timer_start: current_time_past,
            timer_end: current_music_timer_end,
          });
        }
      }
    }
  });
}

var youtubePlayerControl = {
  play: function(options) {
    if(youtubePlayer.initialized) {
      var music_options = {
        videoId: options.musicId,
        suggestedQuality:'default',
      };
      if(options.timer_start){music_options.startSeconds = options.timer_start;}
      if(options.timer_end){music_options.endSeconds = options.timer_end;}
      youtubePlayer.loadVideoById(music_options);
      $(document).attr('title', options.name);
      $('#youtubePlayer').fadeIn(250);
      $( "#slider-vertical" ).fadeIn(250);
    }
  },
  stop: function() {
    if(youtubePlayer.initialized) {
      youtubePlayer.stopVideo();
      $('#youtubePlayer').fadeOut(250);
      $( "#slider-vertical" ).fadeOut(250);
    }
  },
  volume_up: function() {
    if(youtubePlayer.initialized) {
      youtubePlayer.setVolume(Math.min(youtubePlayer.getVolume() + 10, 100));
    }
  },
  volume_down: function() {
    if(youtubePlayer.initialized) {
      youtubePlayer.setVolume(Math.max(youtubePlayer.getVolume() - 10, 0));
    }
  },
  set_volume: function(volume) {
    if (youtubePlayer.initialized ) {
      youtubePlayer.setVolume(volume);
    }
  },
  get_volume: function() {
    if (youtubePlayer.initialized ) {
      return youtubePlayer.getVolume();
    }
    return 10
  }
};
