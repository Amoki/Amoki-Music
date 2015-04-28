var playerControlWrapper = {
  Youtube: youtubePlayerControl,
  Soundcloud: soundcloudPlayerControl,
};

socket.on('message', function(message) {
  if(message.stop) {
    // Stop all players
    Object.keys(playerControlWrapper).forEach(function(player) {
      playerControlWrapper[player].stop();
    });
  }
  if(message.action){
    // stop all others players
    Object.keys(playerControlWrapper).forEach(function(player) {
      if(player !== message.source) {
        playerControlWrapper[player].stop();
      }
    });
    playerControlWrapper[message.source][message.action](message.options);
  }
});
