var pageSize = 40;

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

  if(Cookies.get('room_token') && Cookies.get('room_heartbeat') && Cookies.get('room_wsUri')) {
    setRoomConnexion(Cookies.get('room_token'), Cookies.get('room_heartbeat'), Cookies.get('room_wsUri'));
  }
  else {
    loginVM.isConnected(false);
    loginVM.getRooms();
  }
});

$(document).on('click', '.ordering-to-top, .ordering-move-up, .ordering-move-down, .ordering-to-bot', function() {
  var pk = $(this).closest("tr").attr("id");
  var action = $(this).data("action");
  roomVM.postPlaylistSort(pk, action);
});


function onWsOpen() {
  loginVM.isConnected(true);
  roomVM.getRoom();
  roomVM.getPlaylist();
  musicsLibraryVM.init();
}

// receive a message though the websocket from the server
function receiveMessage(message) {
  message = JSON.parse(message);
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
