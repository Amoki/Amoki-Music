// Youtube iframe init
var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var youtubePlayer = {initialized: false};

var youtubePlayerControl = {
  play: function(options) {
    if(youtubePlayer.initialized) {
      var musicOptions = {
        videoId: options.musicId,
        suggestedQuality: 'default',
      };
      if(options.timerStart) {
        musicOptions.startSeconds = options.timerStart;
      }
      if(options.timerEnd) {
        musicOptions.endSeconds = options.timerEnd;
      }
      youtubePlayer.loadVideoById(musicOptions);
      $(document).attr('title', options.name);
      $('#youtubePlayer').fadeIn(250);
    }
  },
  stop: function() {
    if(youtubePlayer.initialized) {
      youtubePlayer.stopVideo();
      $('#youtubePlayer').fadeOut(250);
    }
  },
  volumeUp: function() {
    if(youtubePlayer.initialized) {
      youtubePlayer.setVolume(Math.min(youtubePlayer.getVolume() + 10, 100));
    }
  },
  volumeDown: function() {
    if(youtubePlayer.initialized) {
      youtubePlayer.setVolume(Math.max(youtubePlayer.getVolume() - 10, 0));
    }
  },
  setVolume: function(volume) {
    if(youtubePlayer.initialized) {
      youtubePlayer.setVolume(volume);
    }
  },
};

// This function creates an <iframe> (and YouTube player)
// after the API code downloads.
function onYouTubeIframeAPIReady() {
  youtubePlayer = new YT.Player('youtubePlayer', {
    height: '390',
    width: '640',
    playerVars: {
      iv_load_policy: '3',
      modestbranding: '1',
      rel: '0',
      controls: '0',
    },
    events: {
      onReady: function() {
        youtubePlayer.initialized = true;
        youtubePlayerControl.setVolume(cookieVolume);
        if(typeof currentMusic !== "undefined" && currentMusicSource === "Youtube") {
          youtubePlayerControl.play({
            musicId: currentMusic,
            timerStart: currentTimePast,
            timerEnd: currentMusicTimerEnd,
          });
        }
      },
    }
  });
}
