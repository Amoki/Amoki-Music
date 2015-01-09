var csrftoken = $.cookie('csrftoken');

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
beforeSend: function(xhr, settings) {
  if(!csrfSafeMethod(settings.type) && !this.crossDomain) {
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
  }
}
});

$(document).on('submit', '.ajax-shuffle', function(e) {
  e.preventDefault();
  var form =  $(this);
  var urlSubmit = form.attr('action');
  var dataSend = 'shuffle=' + encodeURIComponent(form.children("button").val());

  $.ajax({
    type: "POST",
    url: urlSubmit,
    data: dataSend,
    dataType: "json",
    success: function(data) {
      if(data.shuffle === true) {
        modal_confirm($('#modal-shuffle-on'));
      }
      else {
        modal_confirm($('#modal-shuffle-off'));
      }
    },
    error: function(resultat, statut, erreur) {
      log_errors(resultat, statut, erreur);
    },
  });
});


$(document).on('submit', '.ajax-next, .ajax-dead-link', function(e) {
  e.preventDefault();
  var form =  $(this);
  var urlSubmit = form.attr('action');
  var dataSend = 'music_id=' + encodeURIComponent(form.children('.music_id').val());

  $.ajax({
    type: "POST",
    url: urlSubmit,
    data: dataSend,
    dataType: "json",
    success: function(data) {
      modal_confirm($('#modal-next-music'));
    },
    error: function(resultat, statut, erreur) {
      log_errors(resultat, statut, erreur);
    },
  });
});

$(document).on('submit', '.ajax-search', function(e) {
  e.preventDefault();
  var form =  $(this);

  if(form.children('.query').val().trim() === '' || form.children('.query').val().trim() === null) {
    $("#list-youtube").slideUp();
    $("#list-youtube").promise().done(function() {
      $("#list-youtube").children().remove();
      $("#list-youtube").append('<li class="list-group-item item-lib youtube-list-music"><div class="row"><p class="col-xs-10">Enter your search in the field above</p><i class="fa fa-level-up fa-2x col-xs-2"></i></div></li>');
      $("#list-youtube").slideDown();
    });
    return;
  }
  form.children("span").children("button").children("i").attr("class", "fa fa-refresh fa-spin");
  form.children("span").children("button").attr('disabled', 'disabled');
  var urlSubmit = form.attr('action');
  var dataSend = 'query=' + encodeURIComponent(form.children('.query').val());

  $.ajax({
      type: "POST",
      url: urlSubmit,
      data: dataSend,
      dataType: "json",
      success: function(data) {
        if(data.current_music) {
          $("#btn-search").children("i").attr("class", "fa fa-youtube-play");
          $("#btn-search").removeAttr('disabled');
          modal_confirm($('#modal-add-music'));
        }
        else {
          $("#tab_btn_youtube").addClass("active");
          $("#youtube").addClass("active");
          $("#tab_btn_library").removeClass("active");
          $("#library").removeClass("active");
          $("#list-youtube").slideUp();
          $("#list-youtube").promise().done(function() {
            $(".youtube-list-music").remove();
            $("#list-youtube").html(data.template_library);
            $("#list-youtube").slideDown();
            $("#list-youtube").promise().done(function() {
              $("#btn-search").children("i").attr("class", "fa fa-youtube-play");
              $("#btn-search").removeAttr('disabled');
            });
          });
        }
      },
      error: function(resultat, statut, erreur) {
        log_errors(resultat, statut, erreur);
      },
  });
});

$(document).on('submit', '.ajax-add-music', function(e) {
  e.preventDefault();
  var form =  $(this);
  var urlSubmit = form.attr('action');
  var dataSend = {
    'music_id': encodeURIComponent($(this).children('.music_id').val()),
    'requestId': encodeURIComponent($(this).children('.requestId').val()),
  };
  form.children("button").children("span").attr("class", "fa fa-refresh fa-spin");
  form.children("button").attr('disabled', 'disabled');

  $.ajax({
      type: "POST",
      url: urlSubmit,
      data: dataSend,
      dataType: "json",
      success: function(data) {
        form.children("button").children("span").attr('class', 'glyphicon glyphicon-headphones');
        form.children("button").removeAttr('disabled');
        modal_confirm($('#modal-add-music'));
      },
      error: function(resultat, statut, erreur) {
        log_errors(resultat, statut, erreur);
      },
  });
});

$(document).on('submit', '.ajax-volume', function(e) {
  e.preventDefault();
  var form =  $(this);
  var urlSubmit = form.attr('action');
  var dataSend = 'volume_change=' + encodeURIComponent(form.children(".volume_clicked").val());

  $.ajax({
    type: "POST",
    url: urlSubmit,
    data: dataSend,
    dataType: "json",
    success: function(data) {
      form.children(".volume_clicked").removeClass("volume_clicked");
    },
    error: function(resultat, statut, erreur) {
      log_errors(resultat, statut, erreur);
    },
  });
});

$(document).on('submit', '.ajax_music_inifite_scroll', function(e) {
  e.preventDefault();
  var form =  $(this);
  var urlSubmit = form.attr('action');
  var dataSend = 'page=' + encodeURIComponent(form.children("#page").val());
  $("<li id='spinner_library' class='list-group-item item-lib row row-list-item' style='color:black'><i class='fa fa-spinner fa-4x fa-spin'></i></li>").insertBefore(form.closest('li'));

  $.ajax({
    type: "POST",
    url: urlSubmit,
    data: dataSend,
    dataType: "json",
    success: function(data) {
      $(data.template).insertBefore(form.closest('li'));
      if(data.more_musics) {
        form.children("#page").val(parseInt(form.children("#page").val()) + 1);
      }
      else {
        form.children("#page").addClass('disabled');
      }
      $("#spinner_library").remove();
    },
    error: function(resultat, statut, erreur) {
      log_errors(resultat, statut, erreur);
    },
  });
});

function update_player() {
  var dataSend = {
      'page': encodeURIComponent($('.ajax_music_inifite_scroll').children("#page").val()),
    };
  $.ajax({
    type: "POST",
    url: "/update-player/",
    data: dataSend,
    dataType: "json",
    success: function(data) {
      if(data.shuffle === true) {
        $("#btn-shuffle").attr("value", "false");
        $("#btn-shuffle").attr("class", "btn btn-default btn-control btn-shuffle-true");
      }
      else {
        $("#btn-shuffle").attr("value", "true");
        $("#btn-shuffle").attr("class", "btn btn-default btn-control btn-shuffle-false");
      }

      $('.library-list-music').remove();
      $('#list-library').prepend(data.template_library);

      if(data.current_music) {
        timeline(data.time_left, data.time_past_percent);
        maj_playlist_current(data);
      }
      else {
        disabled_btn();
      }
    },
    error: function(resultat, statut, erreur) {
      log_errors(resultat, statut, erreur);
    },
  });
}

function log_errors(resultat, statut, erreur){
  console.log(resultat.responseText);
  console.log("Statut : "+statut);
  console.log("Error : "+erreur);
}

socket.on('message', function(message) {
  if(message.action !== 'volume_up' && message.action !== 'volume_down'){
    update_player();
  }
});
