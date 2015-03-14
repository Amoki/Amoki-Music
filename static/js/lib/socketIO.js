// Socket init
var socket = new io.Socket();
socket.connect();
socket.on('connect', function() {
  socket.subscribe(token);
});
