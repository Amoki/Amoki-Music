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


$(document).on('submit', '.ajax-dead-link', function(e) {
  e.preventDefault();
  var $this = $(this);
  ajax($this).fail(log_errors);
});

function update_player() {
  $.ajax({
    type: "POST",
    url: "/update-player/",
    data: {},
    dataType: "json",
    success: function(data) {
      $('.playlist-ajax').html(data);
    },
    error: log_errors
  });
}

function ajax(source){
  return $.ajax({
    url: source.attr('action'),
    type: source.attr('method'),
    data: source.serialize().replace(/[^&]+=(?:&|$)/gm, ''),
    dataType: "json",
  });
}

function log_errors(resultat, statut, erreur){
  console.error(resultat.responseText);
  console.error("Statut : " + statut);
  console.error("Error: " + erreur.stack);
}
