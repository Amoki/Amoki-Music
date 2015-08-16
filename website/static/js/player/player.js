var playerControlWrapper = {
  Youtube: youtubePlayerControl,
  Soundcloud: soundcloudPlayerControl,
};

// receive a message though the websocket from the server
function receiveMessage(message) {
  message = JSON.parse(message);
  if(message.stop) {
    // Stop all players
    Object.keys(playerControlWrapper).forEach(function(player) {
      playerControlWrapper[player].stop();
      $(document).attr('title', "Amoki's player");
      $('.player-child').not('.player-child-no-music').fadeOut(250);
    });
  }
  if(message.action) {
    // stop all others players
    Object.keys(playerControlWrapper).forEach(function(player) {
      if(player !== message.source) {
        playerControlWrapper[player].stop();
      }
    });
    playerControlWrapper[message.source][message.action](message.options);
  }
  if(message.update === true) {
    updatePlayer();
  }
}

function updateVolume(volume) {
  Object.keys(playerControlWrapper).forEach(function(player) {
    playerControlWrapper[player].set_volume(volume);
  });
}

function displaySlider(value) {
  var offset1 = $("#slider-volume").children('.ui-slider-handle').offset();
  $(".tooltip1").css('top', offset1.top - 120).css('left', offset1.left - 20).text(value);

  var volume = $('#icon-volume');
  if(value === 0) {
    volume.css('background-position', '0 -102px');
  }
  else if(value <= 10) {
    volume.css('background-position', '0 -77px');
  }
  else if(value <= 40) {
    volume.css('background-position', '0 -51px');
  }
  else if(value <= 75) {
    volume.css('background-position', '0 -26px');
  }
  else {
    volume.css('background-position', '0 0');
  }
}

$("#slider-volume").slider({
    range: "min",
    min: 0,
    max: 100,
    create: function() {
      if(typeof cookieVolume !== "undefined") {
        $("#slider-volume").slider("option", "value", cookieVolume);
      }
      else {
        cookieVolume = 10;
        $("#slider-volume").slider("option", "value", 10);
      }
    },
    slide: function(event, ui) {
      updateVolume(ui.value);
      displaySlider(ui.value);
    },
    change: function(event, ui) {
      updateVolume(ui.value);
      displaySlider(ui.value);
      $.cookie('player_volume', ui.value);
    },
    start: function() {
      $(".tooltip1").fadeIn(250);
    },
    stop: function() {
      $(".tooltip1").fadeOut(250);
    },
});

$("#player-wrapper").hover(
    function() {
      if($('.player-child').not('.player-child-no-music').filter(":visible").length > 0) {
        $("#wrapper-slider-volume").fadeIn(300);
      }
    },
    function() {
      $("#wrapper-slider-volume").fadeOut(300);
    }
 );

$('#icon-volume').click(function() {
    $("#slider-volume").slider("option", "value", 0);
  });
