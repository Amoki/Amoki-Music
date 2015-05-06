var playerControlWrapper = {
  Youtube: youtubePlayerControl,
  Soundcloud: soundcloudPlayerControl,
};

jQuery(document).ready(function($) {
  var ws4redis = WS4Redis({
      uri: webSocketUri + token + '?subscribe-broadcast',
      receive_message: receiveMessage,
      heartbeat_msg: ws4redisHeartbeat
  });

  // receive a message though the websocket from the server
  function receiveMessage(message) {
    message = JSON.parse(message);
    if(message.stop) {
      // Stop all players
      Object.keys(playerControlWrapper).forEach(function(player) {
        playerControlWrapper[player].stop();
      });
    }
    if(message.action){
      // stop all others players
      Object.keys(playerControlWrapper).forEach(function(player) {
        console.log(player);
        if(player !== message.source) {
         playerControlWrapper[player].stop();
        }
      });
      playerControlWrapper[message.source][message.action](message.options);
    }
  }
});
