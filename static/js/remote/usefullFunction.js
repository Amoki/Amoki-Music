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
