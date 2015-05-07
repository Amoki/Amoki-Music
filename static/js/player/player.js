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
        $(document).attr('title', "Amoki's player");
        $( "#slider-vertical" ).fadeOut(250);
        $('.player-child').not('.player-child-no-music').fadeOut(250);
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
  }


  $( "#slider-vertical" ).slider({
      orientation: "vertical",
      range: "min",
      min: 0,
      max: 100,
      slide: function( event, ui ) {
        update_volume( ui.value );
        var offset1 = $(this).children( '.ui-slider-handle' ).offset();
        $( ".tooltip1" ).css('top',offset1.top).css('left', offset1.left+25).text(ui.value);
      },
      change: function( event, ui ) {
        update_volume( ui.value );
      },
      start: function( event, ui ) {
        $( ".tooltip1" ).fadeIn(250);
      },
      stop: function( event, ui ) {
        $( ".tooltip1" ).fadeOut(250);
      },
  });

  function update_volume(volume) {
    Object.keys(playerControlWrapper).forEach(function(player) {
      playerControlWrapper[player].set_volume(volume);
    });
  };

});
