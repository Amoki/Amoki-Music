/********************
INIT VARS
INIT AJAX CSRF
********************/
var storeCookie = null;
var getCookie = null;
var removeCookie = null;
if(typeof(Storage) !== "undefined") {
  storeCookie = new Function('key', 'value', 'localStorage.setItem(key, value);');
  getCookie = new Function('key', 'return localStorage.getItem(key);');
  removeCookie = new Function('key', 'localStorage.removeItem(key);');
}
else {
  storeCookie = new Function('key', 'value', 'Cookies.set(key, value, {expires: 7});');
  getCookie = new Function('key', 'return Cookies.get(key);');
  removeCookie = new Function('key', 'Cookies.remove(key);');
}

if(!getCookie('volumePlayer')) {
  storeCookie('volumePlayer', 10);
}

var ws4redis;
function connectWs(token, uri, heartbeat) {
  if(typeof(ws4redis) === "object") {
    ws4redis.close();
  }
  ws4redis = new WS4Redis({
    uri: uri + token + '?subscribe-broadcast',
    onMessage: receiveMessage,
    heartbeat: heartbeat,
    onOpen: onWsOpen,
    onError: onWsError,
    onClose: onWsClose,
  });
}

function setRoomConnexion(token, heartbeat, wsUri) {
  storeCookie('room_token', token);
  $.ajaxSetup({
    beforeSend: function(xhr) {
      xhr.setRequestHeader("Authorization", "Bearer " + token);
    }
  });
  if(heartbeat && wsUri) {
    storeCookie('room_heartbeat', heartbeat);
    storeCookie('room_wsUri', wsUri);
    connectWs(getCookie('room_token'), getCookie('room_wsUri'), getCookie('room_heartbeat'));
  }
  else {
    $.getJSON("/check_credentials",
      function(data) {
        loginVM.isConnected(true);
        storeCookie('room_heartbeat', data.heartbeat);
        storeCookie('room_wsUri', data.uri);
        connectWs(token, data.uri, data.heartbeat);
      }).fail(function(jqxhr) {
        loginVM.badLogin(true);
        console.error(jqxhr.responseText);
        return false;
      }
    );
  }
}

function logOutRoom() {
  removeCookie('room_token');
  removeCookie('room_heartbeat');
  removeCookie('room_wsUri');
  ws4redis.close();
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

function logErrors(resultat, statut, erreur, source) {
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

function modalError(target) {
  target.modal({
    'show': true,
    'backdrop': false
  });
}

/********************
HELPER FUNCTIONS
********************/

String.prototype.capitalize = function() {
  return this.charAt(0).toUpperCase() + this.slice(1);
};

jQuery.fn.noOpacity = function() {
  return this.css('opacity', 0);
};

jQuery.fn.fullOpacity = function() {
  return this.css('opacity', 1);
};

jQuery.fn.opacityToggle = function() {
  return this.css('opacity', function(i, opacity) {
    return (opacity === 1) ? 0 : 1;
  });
};

function arrayFirstIndexOf(array, predicate, predicateOwner) {
  for(var i = 0, j = array.length; i < j; i++) {
    if(predicate.call(predicateOwner, array[i])) {
      return i;
    }
  }
  return -1;
}

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
