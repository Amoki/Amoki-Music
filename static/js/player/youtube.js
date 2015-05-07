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
    playerVars: {iv_load_policy: '3',modestbranding:'1',rel:'0',},
    events: {
      onReady : function(){
        if(typeof current_music !== "undefined" && current_music_source === "Youtube"){
          youtubePlayer.loadVideoById(current_music, current_time_past, 'default');
        }
        youtubePlayer.initialized = true;
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
      $('#youtubePlayer').css("opacity", 1);
    }
  },
  stop: function() {
    if(youtubePlayer.initialized) {
      youtubePlayer.stopVideo();
      $('#youtubePlayer').css("opacity", 0);
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
  }
};
