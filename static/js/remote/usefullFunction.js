$(document).ready(function() {
  var hauteur = $(window).height() - 115;
  if($(window).height() > 765) {
    hauteur = $(window).height() - 115;
  }
  else {
    hauteur = 650;
  }
  $(".LIB").height(hauteur);
  $(".list-lib").height(hauteur - 90);
  $(".tab-content").height(hauteur - 130);
  $(window).resize(function() {
    if($(window).width() > 992) {
      if($(window).height() > 765) {
        hauteur = $(window).height() - 115;
      }
      else {
        hauteur = 650;
      }
      $(".LIB").height(hauteur);
      $(".list-lib").height(hauteur - 90);
      $(".tab-content").height(hauteur - 130);
    }
  });

  $(".btn").click(function() {
    $(this).blur();
  });

  $('.ajax_music_inifite_scroll').submit();

  $("#query").autocomplete({
    minLength: 2,
    source: function(request, response) {
      $.getJSON("http://suggestqueries.google.com/complete/search?callback=?",
        {
        "hl":"fr", // Language
        "ds":"yt", // Restrict lookup to youtube
        "jsonp":"suggestCallBack", // jsonp callback function name
        "q":request.term, // query term
        "client":"youtube" // force youtube style response, i.e. jsonp
        }
      );
      suggestCallBack = function (data) {
        var suggestions = [];
        if (data[1].length > 0) {
          $.each(data[1], function(key, val) {
            val[0] = val[0].substr(0,40);
            suggestions.push({"value":val[0]});
          });
          suggestions.length = 8; // prune suggestions list to only 8 items
          response(suggestions);
        }else{
          $("#query").autocomplete( "close" );
        };
      };
    },
    select: function(event, ui) {
      //assign value back to the form element
      if(ui.item){
          $(event.target).val(ui.item.value);
      }
      //submit the form
      $(event.target.form).submit();
    }
  });

  $('#time-left-progress-bar').countdown('destroy');
  $.countdown.setDefaults({
    compact: true,
  });

  $(document).on("click", ".row-list-item, .show-more", function(e) {
    $(this).siblings('.video-info').slideToggle();
  });
  $(document).on("mouseenter", ".youtube-list-music", function(e) {
    if($(this).children(".video-info").is(":hidden")){
      $(this).children('.show-more').slideDown();
    };
  });
  $(document).on("mouseleave", ".youtube-list-music", function(e) {
    if($(this).children(".video-info").is(":hidden")){
      $(this).children('.show-more').slideUp();
    };
  });

  $(document).on("click", "#btn-preview-duration", function(e) {
    var duration = $(this).data("duration");
    $( "#slider" ).slider( "option", "max", duration );
    $( "#slider" ).slider( "option", "values", [ 0, duration ] );
    playerControl["play"]({musicId:$(this).data("musicid")});
  });
  $('#music_preview').on('hide.bs.modal', function (e) {
    playerControl["stop"]({});
  });

  var playerControl = {
    play: function(options) {
      var music_options = {
        videoId: options.musicId,
        suggestedQuality:'default',
      };
      if(options.timer_start){music_options.startSeconds = options.timer_start};
      if(options.timer_end){music_options.endSeconds = options.timer_end};
      player.loadVideoById(music_options);
      $(document).attr('title', options.name);
    },
    stop: function() {
      player.stopVideo();
    },
    seekTo: function(options){
      player.seekTo(options.secondes, options.seekAhead);
    },
    volume_up: function() {
      player.setVolume(Math.min(player.getVolume() + 10, 100));
    },
    volume_down: function() {
      player.setVolume(Math.max(player.getVolume() - 10, 0));
    }
  };

  var tooltip = $('.tooltip');
  var slider = $( "#slider" );
  tooltip.hide()
  slider.slider({
    range: true,
    min: 0,
    max: 1,
    slide: function( event, ui ) {
      var offset1 = $(this).children('.ui-slider-handle').first().offset();
      var offset2 = $(this).children('.ui-slider-handle').last().offset();
      $(".tooltip1").css('top',offset1.top+30).css('left',offset1.left-5).text(humanize_seconds(ui.values[ 0 ]));
      $(".tooltip2").css('top',offset2.top+30).css('left',offset2.left-5).text(humanize_seconds(ui.values[ 1 ]));

      $( "#time_start" ).html( humanize_seconds(ui.values[ 0 ]) );
      $( "#time_end" ).html( humanize_seconds(ui.values[ 1 ]) );
      /*$( "#timer-start" ).val( humanize_seconds(ui.values[ 0 ]) );
      $( "#timer-end" ).val( humanize_seconds(ui.values[ 1 ]) );*/
      playerControl["seekTo"]({secondes: ui.value, seekAhead: false});
    },
    change: function( event, ui ) {
      $( "#time_start" ).html( humanize_seconds(ui.values[ 0 ]) );
      $( "#time_end" ).html( humanize_seconds(ui.values[ 1 ]) );
      /*$( "#timer-start" ).val( humanize_seconds(ui.values[ 0 ]) );
      $( "#timer-end" ).val( humanize_seconds(ui.values[ 1 ]) );*/
    },
    start: function(event,ui) {
      tooltip.fadeIn('fast');
    },
    stop: function( event, ui ) {
      tooltip.fadeOut('fast');
      playerControl["seekTo"]({secondes: ui.value, seekAhead: true});
    }
  });

});

function maj_header_remote(data) {
  if(data.current_music) {
    $(document).attr('title', data.current_music[0].fields.name);
    $('#music_id-next').val(data.current_music[0].fields.music_id);
    $('#music_id-dead-link').val(data.current_music[0].fields.music_id);
  }
  else {
    disabled_btn();
  }
  $(".player").children('.header-player').html(data.template_header_remote);
}

function disabled_btn() {
  $(document).attr('title', 'Amoki\'s musics');
  $(".header-player").children().remove();
  $('.header-player').append('<div class="col-md-12 title"><div class="marquee"><span class="now-playing">No music :\'( Add yours now !</span></div></div>');
  $("#btn-next").attr('disabled', 'disabled');
  $("#dead-link").attr('disabled', 'disabled');
  $(".progress-bar").stop();
  $(".progress-bar").css('width', '0%');
  $('#time-left-progress-bar').countdown('destroy');
}

function maj_playlist_current(data) {
  $('#time-left-progress-bar').countdown('destroy');
  $("#btn-next").removeAttr('disabled');
  $("#dead-link").removeAttr('disabled');
  $('.playlist-ajax').html(data.template_playlist);
  maj_header_remote(data);
  if(data.current_music) {
    $('#time-left-progress-bar').countdown({until: data.time_left});
  }
}

function modal_confirm(target) {
  target.modal({
      'show': true,
      'backdrop': false
  }).on('shown.bs.modal', function() {
    setTimeout(function() {
      target.modal('hide');
    }, 1000);
  });
}

function timeline(current_time_left, current_time_past_percent){
  $(".progress-bar").stop();
  var actual_time = current_time_left;
  actual_time *= 1000;
  $(".progress-bar").width(current_time_past_percent+'%');
  $(".progress-bar").animate({ 'width' : '100%'} , {
      duration: actual_time,
      easing: 'linear',
  });
}

function humanize_seconds(s) {
  var fm = [
    Math.floor(s / 60) % 60,
    s % 60
  ];
  if(Math.floor(s / 60 / 60) % 24 > 0){fm.unshift(Math.floor(s / 60 / 60) % 24)};
  return $.map(fm, function(v, i) { return ((v < 10) ? '0' : '') + v; }).join(':');
}
