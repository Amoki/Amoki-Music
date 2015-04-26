var playerControlWrapper = {
  youtube: youtubePlayerControl,
  soundcloud: soundcloudPlayerControl,
};

socket.on('message', function(message) {
  if(message.action){
    playerControlWrapper[message.source][message.action](message.options);
  }
});
