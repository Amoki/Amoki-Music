function stopProgressBar() {
  $('style#expand').remove();
  $('.progress-bar').pauseKeyframe();
  $('.progress-bar').css('width', '0%');
  $('#time-left-progress-bar').countTo('stop').html('');
}

function updateProgressBar(duration, currentTimePast, currentTimePastPercent, currentTimeLeft) {
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

  $('style#expand').remove();
  $('.progress-bar').pauseKeyframe();
  $('.progress-bar').width(currentTimePastPercent + '%');
  $.keyframe.define({
    name: 'expand',
    from: {
      'width': currentTimePastPercent + '%'
    },
    to: {
      'width': '100%'
    }
  });
  $('.progress-bar').playKeyframe(
    'expand ' + currentTimeLeft + 's linear 0s 1 normal none'
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


$(document).ready(function() {
  $(window).resize(function() {
    if($(window).width() > 992) {
      resize();
    }
  });
  resize();

  $('.overlay-playlist').hide();

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
  }).keypress(function(e) {
    (!e) ? e = window.event : null;
    if(e.which === 13) {
      $(this).autocomplete('close');
    }
  });


  $(document).on({
    mouseenter: function() {
      $(this).children('.icon-trash').children('.fa-trash-o').fullOpacity();
    },
    mouseleave: function() {
      $(this).children('.icon-trash').children('.fa-trash-o').noOpacity();
    }
  }, '.playlist-item');

  $('#music_preview').on('hide.bs.modal', function() {
    Object.keys(playerPreviewControlWrapper).forEach(function(player) {
      playerPreviewControlWrapper[player].stop();
    });
  });
});
