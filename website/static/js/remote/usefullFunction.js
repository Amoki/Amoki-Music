function stopProgressBar() {
  $(document).attr('title', 'Amoki\'s musics');
  $('.progress-bar').finish();
  $('.progress-bar').css('width', '0%');
  $('#time-left-progress-bar').countTo('stop');
}

function updateProgressBar(duration, currentTimePast, currentTimePastPercent, currentTimeLeft) {
  $('.progress-bar').finish();
  $('#time-left-progress-bar').countTo({
    from: currentTimePast,
    to: duration,
    speed: currentTimeLeft * 1000,
    refreshInterval: 1000,
    formatter: function(value, options) {
      return humanizeSeconds(value.toFixed(options.decimals));
    },
    onUpdate: function(value) {
      this.attr('currentTimePast', value);
    },
  });
  $('#time-left-progress-bar').countTo('restart');

  $('.progress-bar').width(currentTimePastPercent + '%').animate(
  {
    'width': '100%'
  },
  {
    duration: currentTimeLeft * 1000,
    easing: 'linear',
  }
  );
}

function resize() {
  var hauteur;
  if($(window).height() > 765) {
    hauteur = $(window).height() - ($('#navbar-top').outerHeight(true) + $('footer.foot').outerHeight(true) + 25);
  }
  else {
    hauteur = 650;
  }
  // resize of the remote and the library
  $('.remote, .LIB').height(hauteur);
  $('.list-lib').height(hauteur - 90);
  $('.tab-content').height(hauteur - 130);
  $('.list-lib .panel-playlist').height(hauteur - 160);
  $('.players, .playlist-mid').height(hauteur - 250);
}

var playerPreviewControl = {
  play: function(options) {
    var musicOptions = {
      videoId: options.music_id,
      suggestedQuality: 'default',
    };
    if(options.timerStart) {
      musicOptions.startSeconds = options.timerStart;
    }
    if(options.timerEnd) {
      musicOptions.endSeconds = options.timerEnd;
    }
    previewPlayer.cueVideoById(musicOptions);
  },
  stop: function() {
    previewPlayer.stopVideo();
  },
  seekTo: function(options) {
    previewPlayer.seekTo(options.secondes, options.seekAhead);
  },
  getState: function() {
    if([-1, 0, 5].indexOf(previewPlayer.getPlayerState()) > -1) {
      return 0;
    }
    else {
      return previewPlayer.getPlayerState();
    }
  }
};


var customSlider = {
  slide: function(options) {
    options.element.slider({
      range: true,
      min: 0,
      max: options.max,
      values: options.values,
      create: function() {
        $("#time_start").html(humanizeSeconds(0));
        $("#time_end").html(humanizeSeconds(options.max));
      },
      slide: function(event, ui) {
        var offset1 = $(this).children('.ui-slider-handle').first().offset();
        var offset2 = $(this).children('.ui-slider-handle').last().offset();
        $(".tooltip-preview-timer-start").css('top', offset1.top + 30).css('left', offset1.left - 15).text(humanizeSeconds(ui.values[0]));
        $(".tooltip-preview-timer-end").css('top', offset2.top + 30).css('left', offset2.left - 15).text(humanizeSeconds(ui.values[1]));

        $("#time_start").html(humanizeSeconds(ui.values[0]));
        $("#time_end").html(humanizeSeconds(ui.values[1]));
        if(playerPreviewControl.getState() !== 0) {
          playerPreviewControl.seekTo({secondes: ui.value, seekAhead: false});
        }
      },
      change: function(event, ui) {
        $("#time_start").html(humanizeSeconds(ui.values[0]));
        $("#time_end").html(humanizeSeconds(ui.values[1]));
      },
      start: function() {
        $('.tooltip-preview-timer-start, .tooltip-preview-timer-end').fadeIn('fast');
      },
      stop: function(event, ui) {
        $('.tooltip-preview-timer-start, .tooltip-preview-timer-end').fadeOut('fast');
        if(playerPreviewControl.getState() !== 0) {
          playerPreviewControl.seekTo({secondes: ui.value, seekAhead: true});
        }
      },
    });
  },
};


$(document).ready(function() {
  $(window).resize(function() {
    if($(window).width() > 992) {
      resize();
    }
  });
  resize();

  $('.overlay-playlist').hide();

  $('body').popover({
    selector: '[data-toggle="popover"]',
    trigger: 'focus',
    html: true,
    placement: 'left',
    content: function() {
      return "<div class='wrapper-popover-add-music'>" +
      "<div>" +
      "<button form='" + $(this).closest('form').attr('id') + "' class='btn btn-default btn-add-music' type='submit' alt='Ajouter à la playlist' title='Ajouter à la playlist'>" +
      "<span class='glyphicon glyphicon-play-circle'></span> Play music" +
      "</button>" +
      "</div>" +
      "<div>" +
      "<button form='" + $(this).closest('form').next('form.display-none').attr('id') + "' href='#music_preview' class='btn btn-default btn-lg' type='submit' alt='Edit duration' title='Edit duration' data-toggle='modal' data-backdrop='static'>" +
      "<span class='glyphicon glyphicon-time'></span> Edit duration" +
      "</button>" +
      "</div>" +
      "</div>";
    }
  });

  $('#querySearch').autocomplete({
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
          $('#querySearch').autocomplete('close');
        }
      };
    },
    select: function(event, ui) {
      $(this).val(ui.item.value).change();
      $(event.target.form).submit();
    },
  });

  $('#music_preview').on('hide.bs.modal', function() {
    playerPreviewControl.stop();
  });
});
