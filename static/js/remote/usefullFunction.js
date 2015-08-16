"use strict";

$(document).ready(function() {

  function resize(){
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

  $("#page").val(current_page);
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
      suggestCallBack = function (data) {
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
    var channel_name = button.data("channelname");
    var description = button.data("description");
    $("#btn-modal-preview-valid").data("musicId", musicId);
    $("#music_preview #music-channel").html("<p>Posted by : " + channel_name + "</p>");
    $("#music_preview #music-description").html("<p>" + description + "</p>");
    custom_slider.slide({
      element: $("#slider"),
      max: duration,
      values: [0, duration],
      musicId: musicId,
    });
    custom_slider.update_options({
      element:$("#slider"),
      option_with_value: {values: [0, duration]},
    });
    playerControl.play({musicId: musicId});
  });
  $('#music_preview').on('hide.bs.modal', function(e) {
    playerControl.stop();
  });
  $(document).on("click", "#btn-modal-preview-cancel", function(e) {
    $(".input-reset").val("");
  });
  $(document).on('click', '#btn-modal-preview-valid', function(e) {
    $("#form-add-" + $(this).data("musicId")).submit();
  });

  var playerControl = {
    play: function(options) {
      var music_options = {
        videoId: options.musicId,
        suggestedQuality: 'default',
      };
      if(options.timer_start) {
        music_options.startSeconds = options.timer_start;
      }
      if(options.timer_end) {
        music_options.endSeconds = options.timer_end;
      }
      player.cueVideoById(music_options);
    },
    stop: function() {
      player.stopVideo();
    },
    seekTo: function(options) {
      player.seekTo(options.secondes, options.seekAhead);
    },
    volume_up: function() {
      player.setVolume(Math.min(player.getVolume() + 10, 100));
    },
    volume_down: function() {
      player.setVolume(Math.max(player.getVolume() - 10, 0));
    },
    get_state: function() {
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
  var custom_slider = {
    slide: function(options) {
      var musicId = options.musicId;
      options.element.slider({
        range: true,
        min: 0,
        max: options.max,
        slide: function(event, ui) {
          var offset1 = $(this).children('.ui-slider-handle').first().offset();
          var offset2 = $(this).children('.ui-slider-handle').last().offset();
          $(".tooltip1").css('top', offset1.top + 30).css('left', offset1.left - 15).text(humanize_seconds(ui.values[0]));
          $(".tooltip2").css('top', offset2.top + 30).css('left', offset2.left - 15).text(humanize_seconds(ui.values[1]));

          $("#time_start").html(humanize_seconds(ui.values[0]));
          $("#time_end").html(humanize_seconds(ui.values[1]));
          if(playerControl.get_state() !== 0) {
            playerControl.seekTo({secondes: ui.value, seekAhead: false});
          }
        },
        change: function(event, ui) {
          $("#time_start").html(humanize_seconds(ui.values[0]));
          $("#time_end").html(humanize_seconds(ui.values[1]));
          $("#timer-start-" + musicId).val(ui.values[0]);
          $("#timer-end-" + musicId).val(ui.values[1]);
        },
        start: function(event, ui) {
          tooltip.fadeIn('fast');
        },
        stop: function(event, ui) {
          tooltip.fadeOut('fast');
          if(playerControl.get_state() !== 0) {
            playerControl.seekTo({secondes: ui.value, seekAhead: true});
          }
        },
      });
    },
    update_options: function(options) {
      var option_to_update = options.option_with_value;
      for(var option_value in option_to_update) {
        options.element.slider("option", option_value, option_to_update[option_value]);
      }
    },
  };

  $('.btn-change-source').on('click', function () {
    source_selected = $(this).val();
    $('.source-selected').html(source_selected);
    $('#input-source-selected').val(source_selected);
    $('.ajax-search').submit();
  });

});

function maj_header_remote(data) {
  if(data.current_music) {
    $(document).attr('title', data.current_music.name);
    $('#music_id-next').val(data.current_music.music_id);
    $('#music_id-dead-link').val(data.current_music.music_id);
  }
  else {
    disabled_btn();
  }
  $(".remote").children('.header-remote').html(data.template_header_remote);
}

function disabled_btn() {
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

function maj_playlist_current(data) {
  $('#time-left-progress-bar').countdown('destroy');[
  $('#time-left-progress-bar-wrapper').addClass('visibility-hidden');
  $("#btn-next").removeAttr('disabled');
  $("#dead-link").removeAttr('disabled');
  $('.playlist-ajax').html(data.template_playlist);
  maj_header_remote(data);
  if(data.current_music) {
    maj_progress_bar(data);
  }
}

function maj_progress_bar(data) {
  $('#time-left-progress-bar-wrapper').removeClass('visibility-hidden');
  $('#time-left-progress-bar').countdown({
    since: -data.current_time_past,
    onTick: function(periods) {
      if ((data.current_music.duration) === (periods[4] * 3600 + periods[5] * 60 + periods[6])) {
        $('#time-left-progress-bar-wrapper').addClass('visibility-hidden');
        $('#time-left-progress-bar').countdown('destroy');
      }
    },
  });
  $('#time-left-progress-bar-duration').html("/ " + humanize_seconds(data.current_music.duration))
}

function timeline(current_time_left, current_time_past_percent) {
  $(".progress-bar").finish();
  var actual_time = current_time_left;
  actual_time *= 1000;
  $(".progress-bar").width(current_time_past_percent + '%');
  $(".progress-bar").animate({'width': '100%'} , {
      duration: actual_time,
      easing: 'linear',
  });
}

function humanize_seconds(s) {
  var fm = [
    Math.floor(s / 60) % 60,
    s % 60
  ];
  if(Math.floor(s / 60 / 60) % 24 > 0) {
    fm.unshift(Math.floor(s / 60 / 60) % 24);
  }
  return $.map(fm, function(v, i) {
    return ((v < 10) ? '0' : '') + v;
  }).join(':');
}
