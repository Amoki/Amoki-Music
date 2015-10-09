/********************
  INIT VARS
  INIT AJAX CSRF
********************/
if(!Cookies.get('volumePlayer')) {
  Cookies.set('volumePlayer', 10);
}
var csrftoken = Cookies.get('csrftoken');
function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function setRoomConnexion(token, heartbeat, wsUri) {
  Cookies.set('room_token', token);
  Cookies.set('room_heartbeat', heartbeat);
  Cookies.set('room_wsUri', wsUri);
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if(!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
      xhr.setRequestHeader("Authorization", "Bearer " + token);
    }
  });
  var ws4redis = new WS4Redis({
    uri: wsUri + token + '?subscribe-broadcast',
    receive_message: receiveMessage,
    heartbeat_msg: heartbeat,
    onOpen: onWsOpen,
  });
}

/********************
  AJAX SKELETON DECLARATION
********************/
function ajax(source) {
  return $.ajax({
    url: source.attr('action'),
    type: source.attr('method'),
    data: source.serialize().replace(/[^&]+=(?:&|$)/gm, ''),
    dataType: "json",
  });
}

function logErrors(resultat, statut, erreur) {
  console.error(resultat.responseText);
  console.error("Statut : " + statut);
  console.error("Error: " + erreur.stack);
}

/********************
  MODAL WINDOWS
********************/
function modalConfirm(target) {
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
  HELPER FUNCTIONS
********************/

String.prototype.capitalize = function() {
  return this.charAt(0).toUpperCase() + this.slice(1);
};

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
