$(function() {
  loginVM = new LoginViewModel();
  roomVM = new RoomViewModel();
  // Local Binding to avoid multi binding by roomVM and loginVM
  $('.ko-room').each(function(index) {
    ko.applyBindings(roomVM, $('.ko-room')[index]);
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

function onWsOpen() {
  loginVM.isConnected(true);
  roomVM.getRoom();
  roomVM.getPlaylist();
}
