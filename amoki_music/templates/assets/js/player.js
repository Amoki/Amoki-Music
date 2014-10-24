var player;
var initialized = false;
var currentVolume;


// Socket init
var socket = new io.Socket();
socket.connect();
socket.on('connect', function() {
  socket.subscribe(room);
});

socket.on('message', function(message) {
  if(initialized) {
    if(message.action === 'play') {
      player.loadVideoById(message.video_id, 0, 'default');
      $(document).attr('title', message.name);
    }
    if(message.action === "volume_up") {
      currentVolume = player.getVolume();
      if(currentVolume >= 90) {
        player.setVolume(100);
      }
      else {
        player.setVolume(currentVolume + 10);
      }
    }
    if(message.action === "volume_down") {
      currentVolume = player.getVolume();
      if(currentVolume <= 10) {
        player.setVolume(0);
      }
      else {
        player.setVolume(currentVolume - 10);
      }
    }
  }
  if(message.action === 'pause') {
    player.pauseVideo();
  }
  if(message.action === 'resume') {
    player.playVideo();
  }
});

// Youtube iframe init
var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

// 3. This function creates an <iframe> (and YouTube player)
//    after the API code downloads.
function onYouTubeIframeAPIReady() {
  player = new YT.Player('embed', {
    height: '390',
    width: '640',
    videoId: 'M7lc1UVf-VE',
  });
  initialized = true;
}

