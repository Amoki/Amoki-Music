var playerControlWrapper = {
  youtube: youtubePlayerControl,
  soundcloud: soundcloudPlayerControl,
};

var playerPreviewControlWrapper = {
  youtube: youtubePlayerPreviewControl,
  soundcloud: soundcloudPlayerPreviewControl,
};

function updateVolume(volume, doNotCookieSave) {
  Object.keys(playerControlWrapper).forEach(function(player) {
    doNotCookieSave ? null : storeCookie('volumePlayer', volume);
    playerControlWrapper[player] && playerControlWrapper[player].setVolume(volume);
  });
}

function displaySlider(value) {
  var offset1 = $("#slider-volume").children('.ui-slider-handle').offset();
  $(".tooltip-volume-player").css('top', offset1.top - 40).css('left', offset1.left - 5).text(value);

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
    $("#slider-volume").slider("option", "value", getCookie('volumePlayer'));
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

var customSlider = {
  slide: function(options) {
    options.element.slider({
      range: true,
      min: 0,
      max: options.max,
      values: options.values,
      create: function() {
        $("#time_start").html(humanizeSeconds(options.values[0]));
        $("#time_end").html(humanizeSeconds(options.values[1]));
      },
      slide: function(event, ui) {
        var offset1 = $(this).children('.ui-slider-handle').first().offset();
        var offset2 = $(this).children('.ui-slider-handle').last().offset();
        $(".tooltip-preview-timer-start").css('top', offset1.top + 30).css('left', offset1.left - 15).text(humanizeSeconds(ui.values[0]));
        $(".tooltip-preview-timer-end").css('top', offset2.top + 30).css('left', offset2.left - 15).text(humanizeSeconds(ui.values[1]));

        $("#time_start").html(humanizeSeconds(ui.values[0]));
        $("#time_end").html(humanizeSeconds(ui.values[1]));
        if(options.currentPlayerControl.getState() !== 0) {
          options.currentPlayerControl.seekTo({secondes: ui.value, seekAhead: false});
        }
      },
      change: function(event, ui) {
        $("#time_start").html(humanizeSeconds(ui.values[0]));
        $("#time_end").html(humanizeSeconds(ui.values[1]));
      },
      start: function() {
        $('.tooltip-preview-timer-start, .tooltip-preview-timer-end').stop().fadeIn('fast');
      },
      stop: function(event, ui) {
        $('.tooltip-preview-timer-start, .tooltip-preview-timer-end').stop().fadeOut('fast');
        if(options.currentPlayerControl.getState() !== 0) {
          options.currentPlayerControl.seekTo({secondes: ui.value, seekAhead: true});
        }
      },
    });
  },
};
