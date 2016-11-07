"use strict";

function WS4Redis(options) {
  var ws;
  var timer;
  var attempts = 1;
  var heartbeatInterval = null;
  var missedHeartbeats = 0;

  function connect(uri) {
    console.log("Connecting to " + uri + " ...");
    ws = new WebSocket(uri);
    ws.onopen = onOpen;
    ws.onmessage = onMessage;
    ws.onerror = onError;
    ws.onclose = onClose;
    timer = null;
  }

  function sendHeartbeat() {
    missedHeartbeats += 1;
    if(missedHeartbeats > 3) {
      clearInterval(heartbeatInterval);
      heartbeatInterval = null;
      console.warn("Closing connection. Reason: Too many missed heartbeats.");
      ws.close();
    }
    ws.send(options.heartbeat);
  }

  function onOpen() {
    console.log('Connected!');
    // new connection, reset attemps counter
    attempts = 1;
    if(options.heartbeat && heartbeatInterval === null) {
      missedHeartbeats = 0;
      heartbeatInterval = setInterval(sendHeartbeat, 5000);
    }
    return options.onOpen();
  }

  function onClose() {
    console.log("Connection closed!");
    if(!timer) {
      if(attempts > 5) {
        return options.onClose();
      }
      else {
        // try to reconnect
        var interval = generateInteval(attempts);
        timer = setTimeout(function() {
          attempts += 1;
          connect(ws.url);
        }, interval);
      }
    }
  }

  function onError(evt) {
    console.error("Websocket connection is broken!");
    return options.onError(evt);
  }

  function onMessage(evt) {
    if(evt.data === options.heartbeat) {
      // reset the counter for missed heartbeats
      missedHeartbeats = 0;
    }
    else {
      return options.onMessage(JSON.parse(evt.data));
    }
  }

  // this code is borrowed from http://blog.johnryding.com/post/78544969349/
  //
  // Generate an interval that is randomly between 0 and 2^k - 1, where k is
  // the number of connection attmpts, with a maximum interval of 30 seconds,
  // so it starts at 0 - 1 seconds and maxes out at 0 - 30 seconds
  function generateInteval (k) {
    var maxInterval = (Math.pow(2, k) - 1) * 1000;

    // If the generated interval is more than 30 seconds, truncate it down to 30 seconds.
    if(maxInterval > 30 * 1000) {
      maxInterval = 30 * 1000;
    }

    // generate the interval to a random number between 0 and the maxInterval determined from above
    return Math.random() * maxInterval;
  }

  connect(options.uri);

  this.send_message = function(message) {
    ws.send(message);
  };

  this.close = function() {
    // Avoid reconnect
    ws.onclose = function() {};
    // Ignore errors cause of Chrome bad implementation...
    ws.onerror = function() {};
    if(timer) {
      clearInterval(timer);
    }
    if(heartbeatInterval) {
      clearInterval(heartbeatInterval);
    }
    ws.close();
  };
}
