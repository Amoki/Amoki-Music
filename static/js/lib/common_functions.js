/********************
  INIT VARS
  INIT AJAX CSRF
********************/
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

/********************
  AJAX SKELETON DECLARATION
********************/
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

/********************
  AJAX CALLS
********************/
$(document).on('submit', '.ajax-next, .ajax-dead-link', function(e) {
  e.preventDefault();
  var $this = $(this);
  ajax($this).done(function(data) {
    modal_confirm($('#modal-next-music'));
  })
  .fail(log_errors);
});

/********************
  MODAL WINDOWS
********************/
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

/********************
  WEB SOCKET OBJECT DECLARATION
********************/
jQuery(document).ready(function($) {
  var ws4redis = WS4Redis({
      uri: webSocketUri + token + '?subscribe-broadcast',
      receive_message: receiveMessage,
      heartbeat_msg: ws4redisHeartbeat
  });
});
