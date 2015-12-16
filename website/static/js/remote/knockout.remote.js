var pageSize = 40;
var reconnectTry = 0;

$(function() {
  loginVM = new LoginViewModel();
  roomVM = new RoomViewModel();
  musicsLibraryVM = new LibraryViewModel();
  // Local Binding to avoid multi binding by roomVM and musicsLibraryVM
  $('.ko-room').each(function(index) {
    ko.applyBindings(roomVM, $('.ko-room')[index]);
  });
  $('.ko-library').each(function(index) {
    ko.applyBindings(musicsLibraryVM, $('.ko-library')[index]);
  });
  $('.ko-login').each(function(index) {
    ko.applyBindings(loginVM, $('.ko-login')[index]);
  });

  loginVM.getRooms();
  if(getCookie('room_token')) {
    setRoomConnexion(getCookie('room_token'));
  }
  else {
    loginVM.isConnected(false);
  }
});

$(document).on('click', '.ordering-to-top, .ordering-move-up, .ordering-move-down, .ordering-to-bot', function() {
  var pk = $(this).closest("tr").data("pkplaylisttrack");
  var action = $(this).data("action");
  roomVM.postPlaylistSort(pk, action);
});


function onWsOpen() {
  reconnectTry = 0;
  loginVM.wsError(false);
  loginVM.wsConnected(true);
  loginVM.isConnected(true);
  roomVM.init();
  musicsLibraryVM.init();
}

function onWsError() {
  reconnectTry += 1;
  loginVM.wsError(true);
  loginVM.wsConnected(false);
  if(reconnectTry > 10) {
    loginVM.logOut();
  }
}

// receive a message though the websocket from the server
function receiveMessage(message) {
  if(message.stop) {
    // Stop all players
    Object.keys(playerControlWrapper).forEach(function(player) {
      playerControlWrapper[player].stop();
      $('.player-child').not('.player-child-no-music').stop().fadeOut(250);
    });
  }
  if(message.action) {
    if(message.action !== "play" || message.action === "play" && roomVM.playerOpen()) {
      // stop all others players
      Object.keys(playerControlWrapper).forEach(function(player) {
        if(player !== message.source) {
          playerControlWrapper[player].stop();
        }
      });
      playerControlWrapper[message.source][message.action](message.options);
    }
  }
  if(message.update === true) {
    roomVM.getRoom();
    roomVM.getPlaylist();
    musicsLibraryVM.getLibrary();
  }
}

$(document).on('click', '#btn-open-player', function() {
  roomVM.openPlayer();
});
