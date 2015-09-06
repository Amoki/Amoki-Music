function humanizeSeconds(s) {
  var fm = [
    Math.floor(s / 60) % 60,
    s % 60
  ];
  if(Math.floor(s / 60 / 60) % 24 > 0) {
    fm.unshift(Math.floor(s / 60 / 60) % 24);
  }
  return $.map(fm, function(v) {
    return ((v < 10) ? '0' : '') + v;
  }).join(':');
}

function disabledBtn() {
  $(document).attr('title', 'Amoki\'s musics');
  $(".header-remote").children().remove();
  $('.header-remote').append('<div class="col-md-12 title"><div class="marquee"><span class="now-playing">No music :\'( Add yours now !</span></div></div>');
  $("#btn-next").attr('disabled', 'disabled');
  $("#dead-link").attr('disabled', 'disabled');
  $(".progress-bar").stop();
  $(".progress-bar").css('width', '0%');
  $('#time-left-progress-bar').countdown('destroy');
  $('#time-left-progress-bar-wrapper').addClass('visibility-hidden');
}

function updateHeaderRemote(data) {
  if(data.currentMusic) {
    $(document).attr('title', data.currentMusic.name);
    $('#music_id-next').val(data.currentMusic.music_id);
    $('#music_id-dead-link').val(data.currentMusic.music_id);
  }
  else {
    disabledBtn();
  }
  $(".remote").children('.header-remote').html(data.templateHeaderRemote);
}

function updateProgressBar(data) {
  $('#time-left-progress-bar-wrapper').removeClass('visibility-hidden');
  $('#time-left-progress-bar').countdown({
    since: -data.currentTimePast,
    onTick: function(periods) {
      if((data.currentMusic.duration) === (periods[4] * 3600 + periods[5] * 60 + periods[6])) {
        $('#time-left-progress-bar-wrapper').addClass('visibility-hidden');
        $('#time-left-progress-bar').countdown('destroy');
      }
    },
  });
  $('#time-left-progress-bar-duration').html("/ " + humanizeSeconds(data.currentMusic.duration));
}

function updatePlaylistCurrent(data) {
  $('#time-left-progress-bar').countdown('destroy');
  $('#time-left-progress-bar-wrapper').addClass('visibility-hidden');
  $("#btn-next").removeAttr('disabled');
  $("#dead-link").removeAttr('disabled');
  $('.playlist-ajax').html(data.templatePlaylist);
  updateHeaderRemote(data);
  if(data.currentMusic) {
    updateProgressBar(data);
  }
}


function timeline(currentTimeLeft, currentTimePastPercent) {
  $(".progress-bar").finish();
  var actualTime = currentTimeLeft;
  actualTime *= 1000;
  $(".progress-bar").width(currentTimePastPercent + '%');
  $(".progress-bar").animate({'width': '100%'} , {
      duration: actualTime,
      easing: 'linear',
  });
}

function freezeButtons() {
  $("#btn-next, #dead-link").prop('disabled', function(index, value) {
    return !value;
  });
  setTimeout(function() {
    $("#btn-next, #dead-link").prop('disabled', function(index, value) {
      return !value;
    });
  }, 2000);
}

$(document).ready(function() {
  function resize() {
    var hauteur;
    if($(window).height() > 765) {
      hauteur = $(window).height() - ($("#navbar-top").outerHeight(true) + $("footer.foot").outerHeight(true) + 25);
    }
    else {
      hauteur = 650;
    }
    // resize of the remote
    $(".remote").height(hauteur);
    $(".panel-playlist").height(hauteur - 258);
    // resize of the library
    $(".LIB").height(hauteur);
    $(".list-lib").height(hauteur - 90);
    $(".tab-content").height(hauteur - 130);
  }

  $(window).resize(function() {
    if($(window).width() > 992) {
      resize();
    }
  });

  resize();

  $("#overlay-playlist").hide();

  $(".btn").click(function() {
    $(this).blur();
  });

  $('body').popover({
    container: '#popover-container-custom',
    selector: '[data-toggle="popover"]',
    trigger: 'focus',
    html: true,
    placement: 'left',
  });

  $("#page").val(currentPage);
  $('.ajax_music_infinite_scroll').submit();

  $("#query").autocomplete({
    minLength: 2,
    source: function(request, response) {
      $.getJSON("http://suggestqueries.google.com/complete/search?callback=?",
        {
        "hl": "fr", // Language
        "ds": "yt", // Restrict lookup to youtube
        "jsonp": "suggestCallBack", // jsonp callback function name
        "q": request.term, // query term
        "client": "youtube" // force youtube style response, i.e. jsonp
        }
      );
      suggestCallBack = function(data) {
        var suggestions = [];
        if(data[1].length > 0) {
          $.each(data[1], function(key, val) {
            val[0] = val[0].substr(0, 40);
            suggestions.push({"value": val[0]});
          });
          suggestions.length = 8; // prune suggestions list to only 8 items
          response(suggestions);
        }
        else {
          $("#query").autocomplete("close");
        }
      };
    },
    select: function(event, ui) {
      // assign value back to the form element
      if(ui.item) {
        $(event.target).val(ui.item.value);
      }
      // submit the form
      $(event.target.form).submit();
    }
  });

  $('#time-left-progress-bar').countdown('destroy');
  $.countdown.setDefaults({
    compact: true,
    format: 'hMS',
  });

  $('#music_preview').on('show.bs.modal', function(event) {
    var button = $(event.relatedTarget);
    var duration = parseFloat(button.data("duration"));
    var musicId = button.data("musicid");
    var channelName = button.data("channelname");
    var description = button.data("description");
    $("#btn-modal-preview-valid").data("musicId", musicId);
    $("#music_preview #music-channel").html("<p>Posted by : " + channelName + "</p>");
    $("#music_preview #music-description").html("<p>" + description + "</p>");
    customSlider.slide({
      element: $("#slider"),
      max: duration,
      values: [0, duration],
      musicId: musicId,
    });
    customSlider.updateOptions({
      element: $("#slider"),
      optionWithValue: {values: [0, duration]},
    });
    playerControl.play({musicId: musicId});
  });
  $('#music_preview').on('hide.bs.modal', function() {
    playerControl.stop();
  });
  $(document).on("click", "#btn-modal-preview-cancel", function() {
    $(".input-reset").val("");
  });
  $(document).on('click', '#btn-modal-preview-valid', function() {
    $("#form-add-" + $(this).data("musicId")).submit();
  });

  var playerControl = {
    play: function(options) {
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
      player.cueVideoById(musicOptions);
    },
    stop: function() {
      player.stopVideo();
    },
    seekTo: function(options) {
      player.seekTo(options.secondes, options.seekAhead);
    },
    volumeUp: function() {
      player.setVolume(Math.min(player.getVolume() + 10, 100));
    },
    volumeDown: function() {
      player.setVolume(Math.max(player.getVolume() - 10, 0));
    },
    getState: function() {
      if([-1, 0, 5].indexOf(player.getPlayerState()) > -1) {
        return 0;
      }
      else {
        return player.getPlayerState();
      }
    }
  };

  var tooltip = $('.tooltip');
  tooltip.hide();
  var customSlider = {
    slide: function(options) {
      var musicId = options.musicId;
      options.element.slider({
        range: true,
        min: 0,
        max: options.max,
        slide: function(event, ui) {
          var offset1 = $(this).children('.ui-slider-handle').first().offset();
          var offset2 = $(this).children('.ui-slider-handle').last().offset();
          $(".tooltip1").css('top', offset1.top + 30).css('left', offset1.left - 15).text(humanizeSeconds(ui.values[0]));
          $(".tooltip2").css('top', offset2.top + 30).css('left', offset2.left - 15).text(humanizeSeconds(ui.values[1]));

          $("#time_start").html(humanizeSeconds(ui.values[0]));
          $("#time_end").html(humanizeSeconds(ui.values[1]));
          if(playerControl.getState() !== 0) {
            playerControl.seekTo({secondes: ui.value, seekAhead: false});
          }
        },
        change: function(event, ui) {
          $("#time_start").html(humanizeSeconds(ui.values[0]));
          $("#time_end").html(humanizeSeconds(ui.values[1]));
          $("#timer-start-" + musicId).val(ui.values[0]);
          $("#timer-end-" + musicId).val(ui.values[1]);
        },
        start: function() {
          tooltip.fadeIn('fast');
        },
        stop: function(event, ui) {
          tooltip.fadeOut('fast');
          if(playerControl.getState() !== 0) {
            playerControl.seekTo({secondes: ui.value, seekAhead: true});
          }
        },
      });
    },
    updateOptions: function(options) {
      var optionToUpdate = options.optionWithValue;
      for(var optionValue in optionToUpdate) {
        options.element.slider("option", optionValue, optionToUpdate[optionValue]);
      }
    },
  };

  $('.btn-change-source').on('click', function() {
    sourceSelected = $(this).val();
    $('.source-selected').html(sourceSelected);
    $('#input-source-selected').val(sourceSelected);
    $('.ajax-search').submit();
  });


  $( "#sortable" ).sortable({
    placeholder: "ui-state-highlight",
  });
  $( "#sortable" ).disableSelection();

});
