// Socket init
var connected = false;
var timeout;
const RETRY_INTERVAL = 5000;

var socket = new io.Socket();

socket.on('connect', function() {
  socket.subscribe(token);
  connected = true;
  clearTimeout(timeout);
});

socket.on('disconnect', function() {
  connected = false;
  console.log('SocketIo disconnected, trying to automatically to reconnect in ' + RETRY_INTERVAL/1000 + ' seconds.');
  retryConnectOnFailure(RETRY_INTERVAL);
});

var retryConnectOnFailure = function(retryInMilliseconds) {
  timeout = setTimeout(function() {
    if (!connected) {
      socket.connect();
      retryConnectOnFailure(retryInMilliseconds);
    }
  }, retryInMilliseconds);
}

socket.connect();
retryConnectOnFailure(RETRY_INTERVAL);
