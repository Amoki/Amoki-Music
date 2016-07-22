// Youtube iframe init
var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var youtubePlayer = {initialized: false};
var previewYoutubePlayer = {initialized: false};

var youtubePlayerControl = {
  play: function(options) {
    if(youtubePlayer.initialized) {
      var musicOptions = {
        videoId: options.music_id,
        suggestedQuality: 'default',
      };
      if(options.timer_start) {
        musicOptions.startSeconds = options.timer_start;
      }
      youtubePlayer.loadVideoById(musicOptions);
      $('#wrapper-youtube-player').stop().fadeIn(250);
    }
  },
  stop: function() {
    if(youtubePlayer.initialized) {
      youtubePlayer.stopVideo();
      $('#wrapper-youtube-player').stop().fadeOut(250);
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

var youtubePlayerPreviewControl = {
  play: function(options) {
    if(previewYoutubePlayer.initialized) {
      previewYoutubePlayer.cueVideoById({videoId: options.music_id, suggestedQuality: 'default'});
    }
  },
  stop: function() {
    if(previewYoutubePlayer.initialized) {
      previewYoutubePlayer.stopVideo();
    }
  },
  seekTo: function(options) {
    if(previewYoutubePlayer.initialized) {
      previewYoutubePlayer.seekTo(options.secondes, options.seekAhead);
    }
  },
  getState: function() {
    if([-1, 0, 5].indexOf(previewYoutubePlayer.getPlayerState()) > -1) {
      return 0;
    }
    else {
      return previewYoutubePlayer.getPlayerState();
    }
  },
  setVolume: function(volume) {
    if(youtubePlayer.initialized) {
      youtubePlayer.setVolume(volume);
    }
  }
};


// This function creates an <iframe> (and YouTube player)
// after the API code downloads.
function onYouTubeIframeAPIReady() {
  youtubePlayer = new YT.Player('youtubePlayer', {
    height: '100%',
    width: '100%',
    playerVars: {
      iv_load_policy: '3',
      modestbranding: '1',
      rel: '0',
      controls: '0',
    },
    events: {
      onReady: function() {
        youtubePlayer.initialized = true;
        youtubePlayerControl.setVolume(getCookie('volumePlayer'));
        if(getCookie('playerOpen') && getCookie('playerOpen') === "true" && roomVM.room() && roomVM.room().currentMusic() && roomVM.room().currentMusic().source() === "youtube") {
          roomVM.openPlayer();
        }
      },
    }
  });

  previewYoutubePlayer = new YT.Player('preview_player', {
    height: '300px',
    width: '100%',
    playerVars: {
      iv_load_policy: '3',
      modestbranding: '1',
      rel: '0',
      autoplay: '0'
    },
    events: {
      onReady: function() {
        previewYoutubePlayer.initialized = true;
        youtubePlayerPreviewControl.setVolume(getCookie('volumePlayer'));
      },
      onStateChange: function(event) {
        if(event.data === YT.PlayerState.PLAYING) {
          updateVolume(0, true);
        }
      }
    },
  });
}
