var playerControlWrapper = {
  youtube: youtubePlayerControl,
  soundcloud: soundcloudPlayerControl,
};

function updateVolume(volume) {
  Object.keys(playerControlWrapper).forEach(function(player) {
    Cookies.set('volumePlayer', volume);
    playerControlWrapper[player].setVolume(volume);
  });
}

function displaySlider(value) {
  var offset1 = $("#slider-volume").children('.ui-slider-handle').offset();
  $(".tooltip-volume-player").css('top', offset1.top - 40).css('left', offset1.left).text(value);

  var volume = $('#icon-volume');
  if(value === 0) {
    volume.css('background-position', '0 -103px');
  }
  else if(value <= 10) {
    volume.css('background-position', '0 -77px');
  }
  else if(value <= 40) {
    volume.css('background-position', '0 -52px');
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
    $("#slider-volume").slider("option", "value", Cookies.get('volumePlayer'));
  },
  slide: function(event, ui) {
    updateVolume(ui.value);
    displaySlider(ui.value);
  },
  change: function(event, ui) {
    updateVolume(ui.value);
    displaySlider(ui.value);
  },
  start: function() {
    $(".tooltip-volume-player").stop().fadeIn(250);
  },
  stop: function() {
    $(".tooltip-volume-player").stop().fadeOut(250);
  },
});

$("#player-wrapper").hover(
  function() {
    if($('.player-child').not('.player-child-no-music').filter(":visible").length > 0) {
      $("#wrapper-slider-volume").stop().fadeIn(300);
    }
  },
  function() {
    $("#wrapper-slider-volume").stop().fadeOut(300);
  }
  );

$('#icon-volume').click(function() {
  $("#slider-volume").slider("option", "value", 0);
});
