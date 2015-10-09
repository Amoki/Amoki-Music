function WS4Redis(options, $) {
  'use strict';
  var opts, ws, deferred, timer, attempts = 1;
  var heartbeatInterval = null, missedHeartbeats = 0;

  function connect(uri) {
    try {
      console.log("Connecting to " + uri + " ...");
      deferred = $.Deferred();
      ws = new WebSocket(uri);
      ws.onopen = onOpen;
      ws.onmessage = onMessage;
      ws.onerror = onError;
      ws.onclose = onClose;
      timer = null;
    } catch (err) {
      deferred.reject(new Error(err));
    }
  }

  function sendHeartbeat() {
    try {
      missedHeartbeats += 1;
      if(missedHeartbeats > 3) {
        throw new Error("Too many missed heartbeats.");
      }
      ws.send(opts.heartbeat_msg);
    } catch(e) {
      clearInterval(heartbeatInterval);
      heartbeatInterval = null;
      console.warn("Closing connection. Reason: " + e.message);
      ws.close();
    }
  }

  function onOpen() {
    console.log('Connected!');
    // new connection, reset attemps counter
    attempts = 1;
    deferred.resolve();
    if(opts.heartbeat_msg && heartbeatInterval === null) {
      missedHeartbeats = 0;
      heartbeatInterval = setInterval(sendHeartbeat, 5000);
    }
    if(typeof opts.onOpen === 'function') {
      return opts.onOpen();
    }
  }

  function onClose() {
    console.log("Connection closed!");
    if(!timer) {
      // try to reconnect
      var interval = generateInteval(attempts);
      timer = setTimeout(function() {
        attempts += 1;
        connect(ws.url);
      }, interval);
    }
  }

  function onError(evt) {
    console.error("Websocket connection is broken!");
    deferred.reject(new Error(evt));
  }

  function onMessage(evt) {
    if(opts.heartbeat_msg && evt.data === opts.heartbeat_msg) {
      // reset the counter for missed heartbeats
      missedHeartbeats = 0;
    }
    else {
      if(typeof opts.receive_message === 'function') {
        return opts.receive_message(evt.data);
      }
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

  if(this === undefined) {
    return new WS4Redis(options, $);
  }
  if(options.uri === undefined) {
    throw new Error('No Websocket URI in options');
  }
  if($ === undefined) {
    $ = jQuery;
  }

  opts = $.extend({heartbeat_msg: null}, options);
  connect(opts.uri);

  this.send_message = function(message) {
    ws.send(message);
  };

  this.close = function() {
    ws.onclose = function() {};
    ws.close();
  };
}
