var ws4redis;
var pageSize = 40;
var reconnectTry = 0;
var sortableOptions = {
  axis: "y",
  revert: true,
  cursor: "move",
  scrollSpeed: 5,
  delay: 150,
  over: function() {
    $(this).find('.ui-sortable-helper').appendTo(this);
  },
};

var customSlider = {
  slide: function(options) {
    options.element.slider({
      range: true,
      min: 0,
      max: options.max,
      values: options.values,
      create: function() {
        $("#time_start").html(humanizeSeconds(options.values[0]));
        $("#time_end").html(humanizeSeconds(options.values[1]));
      },
      slide: function(event, ui) {
        var offset1 = $(this).children('.ui-slider-handle').first().offset();
        var offset2 = $(this).children('.ui-slider-handle').last().offset();
        $(".tooltip-preview-timer-start").css('top', offset1.top + 30).css('left', offset1.left - 15).text(humanizeSeconds(ui.values[0]));
        $(".tooltip-preview-timer-end").css('top', offset2.top + 30).css('left', offset2.left - 15).text(humanizeSeconds(ui.values[1]));

        $("#time_start").html(humanizeSeconds(ui.values[0]));
        $("#time_end").html(humanizeSeconds(ui.values[1]));
        if(options.currentPlayerControl.getState() !== 0) {
          options.currentPlayerControl.seekTo({secondes: ui.value, seekAhead: false});
        }
      },
      change: function(event, ui) {
        $("#time_start").html(humanizeSeconds(ui.values[0]));
        $("#time_end").html(humanizeSeconds(ui.values[1]));
      },
      start: function() {
        $('.tooltip-preview-timer-start, .tooltip-preview-timer-end').stop().fadeIn('fast');
      },
      stop: function(event, ui) {
        $('.tooltip-preview-timer-start, .tooltip-preview-timer-end').stop().fadeOut('fast');
        if(options.currentPlayerControl.getState() !== 0) {
          options.currentPlayerControl.seekTo({secondes: ui.value, seekAhead: true});
        }
      },
    });
  },
};

// Youtube iframe init
var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var youtubePlayer = {initialized: false};
var previewYoutubePlayer = {initialized: false};

var youtubePlayerControl = {
  play: function(options) {
    if(youtubePlayer.initialized) {
      var musicOptions = {
        videoId: options.music_id,
        suggestedQuality: 'default',
      };
      if(options.timer_start) {
        musicOptions.startSeconds = options.timer_start;
      }
      youtubePlayer.loadVideoById(musicOptions);
      $('#wrapper-youtube-player').stop().fadeIn(250);
    }
  },
  stop: function() {
    if(youtubePlayer.initialized) {
      youtubePlayer.stopVideo();
      $('#wrapper-youtube-player').stop().fadeOut(250);
    }
  },
  volumeUp: function() {
    if(youtubePlayer.initialized) {
      youtubePlayer.setVolume(Math.min(youtubePlayer.getVolume() + 10, 100));
    }
  },
  volumeDown: function() {
    if(youtubePlayer.initialized) {
      youtubePlayer.setVolume(Math.max(youtubePlayer.getVolume() - 10, 0));
    }
  },
  setVolume: function(volume) {
    if(youtubePlayer.initialized) {
      youtubePlayer.setVolume(volume);
    }
  },
};

var youtubePlayerPreviewControl = {
  play: function(options) {
    if(previewYoutubePlayer.initialized) {
      previewYoutubePlayer.cueVideoById({videoId: options.music_id, suggestedQuality: 'default'});
    }
  },
  stop: function() {
    if(previewYoutubePlayer.initialized) {
      previewYoutubePlayer.stopVideo();
    }
  },
  seekTo: function(options) {
    if(previewYoutubePlayer.initialized) {
      previewYoutubePlayer.seekTo(options.secondes, options.seekAhead);
    }
  },
  getState: function() {
    if([-1, 0, 5].indexOf(previewYoutubePlayer.getPlayerState()) > -1) {
      return 0;
    }
    else {
      return previewYoutubePlayer.getPlayerState();
    }
  }
};


// This function creates an <iframe> (and YouTube player)
// after the API code downloads.
function onYouTubeIframeAPIReady() {
  youtubePlayer = new YT.Player('youtubePlayer', {
    height: '100%',
    width: '100%',
    playerVars: {
      iv_load_policy: '3',
      modestbranding: '1',
      rel: '0',
      controls: '0',
    },
    events: {
      onReady: function() {
        youtubePlayer.initialized = true;
        youtubePlayerControl.setVolume(getCookie('volumePlayer'));
        if(getCookie('playerOpen') && getCookie('playerOpen') === "true" && roomVM.room() && roomVM.room().currentMusic() && roomVM.room().currentMusic().source() === "youtube") {
          roomVM.openPlayer();
        }
      },
    }
  });

  previewYoutubePlayer = new YT.Player('preview_player', {
    height: '300px',
    width: '100%',
    playerVars: {
      iv_load_policy: '3',
      modestbranding: '1',
      rel: '0',
      autoplay: '0'
    },
    events: {
      onReady: function() {
        previewYoutubePlayer.initialized = true;
      },
    },
  });
}


var iframeElement = document.querySelector('iframe#soundcloudPlayer');
var iframeElementPreview = document.querySelector('iframe#soundcloudPreviewPlayer');
var soundcloudPlayer = SC.Widget(iframeElement);
var soundcloudPreviewPlayer = SC.Widget(iframeElementPreview);
soundcloudPlayer.initialized = false;
soundcloudPreviewPlayer.initialized = false;

soundcloudPlayer.bind(SC.Widget.Events.READY, function() {
  soundcloudPlayer.initialized = true;
  if(getCookie('playerOpen') && getCookie('playerOpen') === "true" && roomVM.room() && roomVM.room().currentMusic() && roomVM.room().currentMusic().source() === "soundcloud") {
    roomVM.openPlayer();
  }
});
soundcloudPreviewPlayer.bind(SC.Widget.Events.READY, function() {
  soundcloudPreviewPlayer.initialized = true;
});

soundcloudPlayer.bind(SC.Widget.Events.ERROR, function() {
  if($('iframe#soundcloudPlayer').is(":visible")) {
    console.error("Soundcloud error occured");
  }
});
soundcloudPreviewPlayer.bind(SC.Widget.Events.ERROR, function() {
  if($('iframe#soundcloudPreviewPlayer').is(":visible")) {
    console.error("Soundcloud error occured");
  }
});

var soundcloudPlayerControl = {
  play: function(options) {
    if(soundcloudPlayer.initialized) {
      $('#wrapper-soundcloud-player').stop().fadeIn(250);
      soundcloudPlayer.bind(SC.Widget.Events.PLAY, function() {
        soundcloudPlayer.seekTo(options.timer_start * 1000 || 0);
        soundcloudPlayer.unbind(SC.Widget.Events.PLAY);
      });
      soundcloudPlayer.load(
        'https://api.soundcloud.com/tracks/' + options.music_id,
        {
          buying: false,
          visual: true,
          hide_related: true,
          auto_play: true,
          callback: function() {
            soundcloudPlayer.setVolume(getCookie('volumePlayer') / 100);
          },
        }
        );
    }
  },
  stop: function() {
    if(soundcloudPlayer.initialized) {
      soundcloudPlayer.pause();
      $('#wrapper-soundcloud-player').stop().fadeOut(250);
    }
  },
  volumeUp: function() {
    if(soundcloudPlayer.initialized) {
      soundcloudPlayer.getVolume(function(volume) {
        soundcloudPlayer.setVolume(Math.min(volume + 0.1, 1));
      });
    }
  },
  volumeDown: function() {
    if(soundcloudPlayer.initialized) {
      soundcloudPlayer.getVolume(function(volume) {
        soundcloudPlayer.setVolume(Math.max(volume - 0.1, 0));
      });
    }
  },
  setVolume: function(volume) {
    if(soundcloudPlayer.initialized) {
      soundcloudPlayer.setVolume(volume / 100);
    }
  },
};

var soundcloudPlayerPreviewControl = {
  play: function(options) {
    if(soundcloudPreviewPlayer.initialized) {
      soundcloudPreviewPlayer.load(
        'https://api.soundcloud.com/tracks/' + options.music_id,
        {
          buying: false,
          visual: true,
          hide_related: true,
        }
      );
    }
  },
  stop: function() {
    if(soundcloudPreviewPlayer.initialized) {
      soundcloudPreviewPlayer.pause();
    }
  },
  seekTo: function(options) {
    if(soundcloudPreviewPlayer.initialized) {
      soundcloudPreviewPlayer.seekTo(options.secondes * 1000);
    }
  },
  getState: function() {
    return 1;
  }
};

var playerControlWrapper = {
  youtube: youtubePlayerControl,
  soundcloud: soundcloudPlayerControl,
};

var playerPreviewControlWrapper = {
  youtube: youtubePlayerPreviewControl,
  soundcloud: soundcloudPlayerPreviewControl,
};

(function(factory) {
  if(typeof define === 'function' && define.amd) {
    // AMD
    define(['jquery'], factory);
  }
  else if(typeof exports === 'object') {
    // CommonJS
    factory(require('jquery'));
  }
  else {
    // Browser globals
    factory(jQuery);
  }
}(function($) {
  var CountTo = function(element, options) {
    this.$element = $(element);
    this.options  = $.extend({}, CountTo.DEFAULTS, this.dataOptions(), options);
    this.init();
  };

  function formatter(value, options) {
    return value.toFixed(options.decimals);
  }

  CountTo.DEFAULTS = {
    from: 0,               // the number the element should start at
    to: 0,                 // the number the element should end at
    speed: 1000,           // how long it should take to count between the target numbers
    refreshInterval: 100,  // how often the element should be updated
    decimals: 0,           // the number of decimal places to show
    formatter: formatter,  // handler for formatting the value before rendering
    onUpdate: null,        // callback method for every time the element is updated
    onComplete: null       // callback method for when the element finishes updating
  };

  CountTo.prototype.init = function() {
    this.value     = this.options.from;
    this.loops     = Math.ceil(this.options.speed / this.options.refreshInterval);
    this.loopCount = 0;
    this.increment = (this.options.to - this.options.from) / this.loops;
  };

  CountTo.prototype.dataOptions = function() {
    var options = {
      from:            this.$element.data('from'),
      to:              this.$element.data('to'),
      speed:           this.$element.data('speed'),
      refreshInterval: this.$element.data('refresh-interval'),
      decimals:        this.$element.data('decimals')
    };

    var keys = Object.keys(options);

    for(var i in keys) {
      var key = keys[i];

      if(typeof(options[key]) === 'undefined') {
        delete options[key];
      }
    }

    return options;
  };

  CountTo.prototype.update = function() {
    this.value += this.increment;
    this.loopCount += 1;

    this.render();

    if(typeof(this.options.onUpdate) === 'function') {
      this.options.onUpdate.call(this.$element, this.value);
    }

    if(this.loopCount >= this.loops) {
      clearInterval(this.interval);
      this.value = this.options.to;

      if(typeof(this.options.onComplete) === 'function') {
        this.options.onComplete.call(this.$element, this.value);
      }
    }
  };

  CountTo.prototype.render = function() {
    var formattedValue = this.options.formatter.call(this.$element, this.value, this.options);
    this.$element.text(formattedValue);
  };

  CountTo.prototype.restart = function() {
    this.stop();
    this.init();
    this.start();
  };

  CountTo.prototype.start = function() {
    this.stop();
    this.render();
    this.interval = setInterval(this.update.bind(this), this.options.refreshInterval);
  };

  CountTo.prototype.stop = function() {
    if(this.interval) {
      clearInterval(this.interval);
    }
  };

  CountTo.prototype.toggle = function() {
    if(this.interval) {
      this.stop();
    }
    else {
      this.start();
    }
  };


  $.fn.countTo = function(option) {
    return this.each(function() {
      var $this   = $(this);
      var data    = $this.data('countTo');
      var init    = !data || typeof(option) === 'object';
      var options = typeof(option) === 'object' ? option : {};
      var method  = typeof(option) === 'string' ? option : 'start';

      if(init) {
        if(data) {
          data.stop();
        }
        $this.data('countTo', data = new CountTo(this, options));
      }

      data[method].call(data);
    });
  };
}));


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
    ws.send(options.heartbeat_msg);
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


/* global define */
function setupKoBootstrap(koObject, $) {
  // Outer HTML
  if(!$.fn.outerHtml) {
    $.fn.outerHtml = function() {
      if(this.length === 0) {
        return false;
      }
      var elem = this[0];
      var name = elem.tagName.toLowerCase();
      if(elem.outerHTML) {
        return elem.outerHTML;
      }
      var attrs = $.map(elem.attributes, function(i) {
        return i.name + '="' + i.value + '"';
      });
      return "<" + name + (attrs.length > 0 ? " " + attrs.join(" ") : "") + ">" + elem.innerHTML + "</" + name + ">";
    };
  }

  // Bind Bootstrap Popover
  koObject.bindingHandlers.popover = {
    init: function(element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) {
      var $element = $(element);
      var popoverBindingValues = koObject.utils.unwrapObservable(valueAccessor());
      var template = popoverBindingValues.template || false;
      var options = popoverBindingValues.options || {title: 'popover'};
      var data = popoverBindingValues.data || false;
      var controlDescendants = popoverBindingValues.controlDescendants;
      if(template !== false) {
        if(data) {
          options.content = "<!-- ko template: { name: template, if: data, data: data } --><!-- /ko -->";
        }
        else {
          options.content = $('#' + template).html();
        }
        options.html = true;
      }
      $element.on('shown.bs.popover', function(event) {

        var popoverData = $(event.target).data();
        var popoverEl = popoverData['bs.popover'].$tip;
        var options = popoverData['bs.popover'].options || {};
        var button = $(event.target);
        var buttonPosition = button.position();
        var buttonDimensions = {
          x: button.outerWidth(),
          y: button.outerHeight()
        };


        koObject.cleanNode(popoverEl[0]);
        if(data) {
          ko.applyBindings({template: template, data: data}, popoverEl[0]);
        }
        else {
          var childBindingContext = bindingContext.createChildContext(
            bindingContext.$rawData,
            null, // Optionally, pass a string here as an alias for the data item in descendant contexts
            function(context) {
              ko.utils.extend(context, valueAccessor());
            }
          );
          ko.applyBindings(childBindingContext, popoverEl[0]);
        }

        var popoverDimensions = {
          x: popoverEl.outerWidth(),
          y: popoverEl.outerHeight()
        };

        popoverEl.find('button[data-dismiss="popover"]').click(function() {
          button.popover('hide');
        });

        switch (options.placement) {
          case 'right':
            popoverEl.css({
              left: buttonDimensions.x + buttonPosition.left,
              top: (buttonDimensions.y / 2 + buttonPosition.top) - popoverDimensions.y / 2
            });
          break;
          case 'left':
            popoverEl.css({
              left: buttonPosition.left - popoverDimensions.x,
              top: (buttonDimensions.y / 2 + buttonPosition.top) - popoverDimensions.y / 2
            });
          break;
          case 'top':
            popoverEl.css({
              left: buttonPosition.left + (buttonDimensions.x / 2 - popoverDimensions.x / 2),
              top: buttonPosition.top - popoverDimensions.y
            });
          break;
          case 'bottom':
            popoverEl.css({
              left: buttonPosition.left + (buttonDimensions.x / 2 - popoverDimensions.x / 2),
              top: buttonPosition.top + buttonDimensions.y
            });
          break;
        }
      });

      $element.popover(options);
      koObject.utils.domNodeDisposal.addDisposeCallback(element, function() {
        $element.popover('destroy');
      });

      return {controlsDescendantBindings: typeof controlDescendants === 'undefined' ? true : controlDescendants};

    }
  };

}

(function(factory) {
  // Support multiple loading scenarios
  if(typeof define === 'function' && define.amd) {
    // AMD anonymous module

    define(["require", "exports", "knockout", "jquery"], function(require, exports, knockout, jQuery) {
      factory(knockout, jQuery);
    });
  }
  else {
    // No module loader (plain <script> tag) - put directly in global namespace
    factory(window.ko, jQuery);
  }
}(setupKoBootstrap));


function onWsOpen() {
  reconnectTry = 0;
  loginVM.wsError(false);
  roomVM.init();
  musicsLibraryVM.init();
  loginVM.wsConnected(true);
}

function onWsError() {
  reconnectTry += 1;
  loginVM.wsError(true);
  loginVM.wsConnected(false);
  if(reconnectTry > 6) {
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


function stopProgressBar() {
  $(document).attr('title', 'Amoki\'s musics');
  $('.progress-bar').finish();
  $('.progress-bar').css('width', '0%');
  $('#time-left-progress-bar').countTo('stop');
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


function updateProgressBar(duration, currentTimePast, currentTimePastPercent, currentTimeLeft) {
  $('.progress-bar').finish();
  $('#time-left-progress-bar').countTo({
    from: currentTimePast,
    to: duration,
    speed: currentTimeLeft * 1000,
    refreshInterval: 1000,
    formatter: function(value, options) {
      return humanizeSeconds(value.toFixed(options.decimals));
    },
    onUpdate: function(value) {
      this.attr('currentTimePast', value);
    },
  });
  $('#time-left-progress-bar').countTo('restart');

  $('.progress-bar').width(currentTimePastPercent + '%').animate(
  {
    'width': '100%'
  },
  {
    duration: currentTimeLeft * 1000,
    easing: 'linear',
  }
  );
}

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
  });
}

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

// function modalError(target) {
//   target.modal({
//     'show': true,
//     'backdrop': false
//   });
// }

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


var afterMoveSortable = function(obj) {
  var action = "";
  var targetPk;
  if(obj.targetIndex < obj.sourceParent().length - 1) {
    action = "above";
    targetPk = obj.sourceParent()[obj.targetIndex + 1].pk();
  }
  else {
    action = "below";
    targetPk = obj.sourceParent()[obj.targetIndex - 1].pk();
  }
  roomVM.postPlaylistSort(obj.item.pk(), action, targetPk);
};

ko.bindingHandlers.stopBinding = {
  init: function() {
    return {controlsDescendantBindings: true};
  }
};
ko.virtualElements.allowedBindings.stopBinding = true;

ko.bindingHandlers.selectPicker = {
  init: function(element, valueAccessor, allBindingsAccessor) {
    if($(element).is('select')) {
      if(ko.isObservable(valueAccessor())) {
        if($(element).prop('multiple') && $.isArray(ko.utils.unwrapObservable(valueAccessor()))) {
          // in the case of a multiple select where the valueAccessor() is an observableArray, call the default Knockout selectedOptions binding
          ko.bindingHandlers.selectedOptions.init(element, valueAccessor, allBindingsAccessor);
        }
        else {
          // regular select and observable so call the default value binding
          ko.bindingHandlers.value.init(element, valueAccessor, allBindingsAccessor);
        }
      }
      $(element).addClass('selectpicker').selectpicker();
    }
  },
  update: function(element, valueAccessor, allBindingsAccessor) {
    if($(element).is('select')) {
      var selectPickerOptions = allBindingsAccessor().selectPickerOptions;
      if(typeof selectPickerOptions !== 'undefined' && selectPickerOptions !== null) {
        var options = selectPickerOptions.optionsArray;
        var isDisabled = selectPickerOptions.disabledCondition || false;
        var resetOnDisabled = selectPickerOptions.resetOnDisabled || false;
        if(ko.utils.unwrapObservable(options).length > 0) {
          // call the default Knockout options binding
          ko.bindingHandlers.options.update(element, options, allBindingsAccessor);
        }
        if(isDisabled && resetOnDisabled) {
          // the dropdown is disabled and we need to reset it to its first option
          $(element).selectpicker('val', $(element).children('option:first').val());
        }
        $(element).prop('disabled', isDisabled);
      }
      if(ko.isObservable(valueAccessor())) {
        if($(element).prop('multiple') && $.isArray(ko.utils.unwrapObservable(valueAccessor()))) {
          // in the case of a multiple select where the valueAccessor() is an observableArray, call the default Knockout selectedOptions binding
          ko.bindingHandlers.selectedOptions.update(element, valueAccessor);
        }
        else {
          // call the default Knockout value binding
          ko.bindingHandlers.value.update(element, valueAccessor);
        }
      }

      $(element).selectpicker('refresh');
    }
  }
};

ko.subscribable.fn.trimmed = function() {
  return ko.computed({
    read: function() {
      if(this()) {
        return this().trim();
      }
    },
    write: function(value) {
      if(value) {
        this(value.trim());
      }
      else {
        this(null);
      }
      this.valueHasMutated();
    },
    owner: this
  });
};

ko.bindingHandlers.visibleKeepDOM = {
  init: function(element) {
    $(element).children().each(function() {
      $(this).hide();
    });
  },
  update: function(element, valueAccessor) {
    var values = ko.unwrap(valueAccessor());
    if(values) {
      $(element).children('.' + values.source()).show();
    }
    else {
      $(element).children().each(function() {
        $(this).fadeOut(1000);
      });
    }
  }
};




// MODEL DEFINITION
// Music model
function Music(data) {
  this.pk = ko.observable(data.pk);
  this.music_id = ko.observable(data.music_id);
  this.name = ko.observable(data.name);
  this.thumbnail = ko.observable(data.thumbnail);
  this.count = ko.observable(data.count || data.views);
  this.total_duration = ko.observable(data.total_duration);
  this.duration = ko.observable(data.duration);
  this.timer_start = ko.observable(data.timer_start);
  this.timer_end = ko.computed(function() {
    return this.timer_start() + this.duration();
  }, this);
  this.url = ko.observable(data.url);
  this.room_id = ko.observable(data.room_id);
  this.source = ko.observable(data.source);
  this.channel_name = ko.observable(data.channel_name);
  this.description = ko.observable(data.description);

  this.from = data.from;
}
// Playlist model
function PlaylistTrack(data) {
  this.pk = ko.observable(data.pk);
  this.order = ko.observable(data.order);
  this.music = ko.observable(new Music(data.music));
}
// Room model
function Room(data) {
  this.name = ko.observable(data.name);
  this.currentMusic = ko.observable(data.current_music ? new Music(data.current_music) : null);
  this.shuffle = ko.observable(data.shuffle);
  this.can_adjust_volume = ko.observable(data.can_adjust_volume);
  this.count_left = ko.observable(data.count_left);
  this.time_left = ko.observable(data.time_left);
  this.current_time_left = ko.observable(data.current_time_left);
  this.current_time_past = ko.observable(data.current_time_past);
  this.current_time_past_percent = ko.observable(data.current_time_past_percent);
}
// Source model
function Source(data) {
  this.name = ko.observable(data.capitalize());
}



// VIEW MODEL DEFINITION
// Library view model
function LibraryViewModel() {
  var self = this;

  // library part
  self.musicsLibrary = ko.observableArray([]);
  self.hasPrevious = ko.observable();
  self.hasNext = ko.observable();
  self.currentPage = ko.observable();

  // search part
  self.musicSearch = ko.observableArray([]);
  self.sourceSearch = ko.observable();
  self.querySearch = ko.observable().trimmed();

  // source part
  self.sources = ko.observableArray([]);

  // preview part
  self.musicPreview = ko.observable();

  self.clear = function() {
    self.musicsLibrary([]);
    self.hasPrevious(null);
    self.hasNext(null);
    self.currentPage(null);
    self.musicSearch([]);
    self.sourceSearch(null);
    self.querySearch(null);
    self.sources([]);
    self.musicPreview(null);
  };

  self.addMusic = function(music) {
    // Return a json serialized Music object
    $.ajax("/music", {
      data: ko.toJSON(music),
      type: "post",
      contentType: "application/json",
      dataType: "json",
      success: function() {
        $("button.btn-add-music").removeClass("icon-refresh").children("span").attr("class", "glyphicon glyphicon-play-circle");
        $("button.btn-add-music").prop('disabled', false);
        modalConfirm($('#modal-add-music'));
      }
    });
  };

  self.patchMusic = function(music, play) {
    // Return a json serialized Music object
    $.ajax("/music/" + music.pk(), {
      data: ko.toJSON(music),
      type: "patch",
      contentType: "application/json",
      dataType: "json",
      success: function() {
        if(!play) {
          $("button.btn-add-music").removeClass("icon-refresh").children("span").attr("class", "glyphicon glyphicon-play-circle");
          $("button.btn-add-music").prop('disabled', false);
          modalConfirm($('#modal-add-music'));
        }
        else {
          self.addMusic(music);
        }
      }
    });
  };

  self.sendMusic = function(music, play) {
    $("button.btn-add-music").addClass("icon-refresh").children("span").attr("class", "fa fa-refresh fa-spin");
    $("button.btn-add-music").prop('disabled', true);
    if(music.from === 'search') {
      self.addMusic(music);
    }
    else if(music.from === 'library') {
      if(play === 'play') {
        self.addMusic(music);
      }
      else {
        self.patchMusic(music, play);
      }
    }
  };

  self.openPreviewMusic = function(music) {
    self.musicPreview(music);
    var handlerStart = self.musicPreview().timer_start() ? self.musicPreview().timer_start() : 0;
    var handlerEnd = self.musicPreview().timer_end() ? self.musicPreview().timer_end() : self.musicPreview().total_duration();
    customSlider.slide({
      element: $("#slider-preview"),
      max: self.musicPreview().total_duration(),
      values: [handlerStart, handlerEnd],
      currentPlayerControl: playerPreviewControlWrapper[music.source()],
    });
    playerPreviewControlWrapper[music.source()].play({music_id: self.musicPreview().music_id()});
  };

  self.closePreviewMusic = function(valid, play) {
    $('#music_preview').modal('hide');
    if(valid) {
      self.musicPreview().timer_start($('#slider-preview').slider("values", 0));
      self.musicPreview().duration(self.musicPreview().total_duration() - self.musicPreview().timer_start() - (self.musicPreview().total_duration() - $('#slider-preview').slider("values", 1)));
      self.sendMusic(self.musicPreview(), play);
    }
    self.musicPreview(null);
  };

  self.deleteMusic = function(music) {
    roomVM.deleteMusic(music);
  };

  self.searchMusic = function() {
    // Return a json serialized Music object
    if(!self.querySearch()) {
      // TODO Display empty field warning
      return;
    }
    $("button.btn-search-icon").children("i").attr("class", "fa fa-refresh fa-spin");
    $("button.btn-search-icon").prop('disabled', true);
    $.getJSON("/search",
    {
      "service": ko.toJS(self.sourceSearch).toLowerCase(),
      "query": self.querySearch()
    },
    function(allData) {
      var mappedMusics = $.map(allData, function(item) {
        item.from = 'search';
        return new Music(item);
      });
      self.musicSearch(mappedMusics);
      $("#tab_btn_library, #library").removeClass('active');
      $("#tab_btn_search, #search-tab").addClass('active');
      $("button.btn-search-icon").children("i").attr("class", "fa fa-search");
      $("button.btn-search-icon").prop('disabled', false);
    }).fail(function(jqxhr) {
      console.error(jqxhr.responseText);
    });
  };

  // Load Library page from server, convert it to Music instances, then populate self.musics
  self.getLibrary = function(target, event) {
    var url;
    event ? url = event.target.value : url = "/musics?page_size=" + pageSize;
    $.getJSON(url, function(allData) {
      var mappedMusics = $.map(allData.results, function(item) {
        item.from = 'library';
        return new Music(item);
      });
      self.musicsLibrary(mappedMusics);
      self.hasPrevious(allData.previous);
      self.hasNext(allData.next);
      $("#popover-container-custom").scrollTop(0);
    }).fail(function(jqxhr) {
      console.error(jqxhr.responseText);
    });
  };

  // Load Sources from server, convert it to Source instances, then populate self.sources
  self.getSources = function() {
    $.getJSON("/sources", function(allData) {
      var mappedSources = $.map(allData, function(item) {
        return new Source(item);
      });
      self.sources(mappedSources);
    }).fail(function(jqxhr) {
      console.error(jqxhr.responseText);
    });
  };

  self.init = function() {
    self.getLibrary();
    self.getSources();
  };
}

// Room view model
function RoomViewModel() {
  var self = this;

  self.room = ko.observable();
  self.playlistTracks = ko.observableArray([]);

  (!getCookie('playerOpen') || getCookie('playerOpen') === false) ? storeCookie('playerOpen', false) : null;
  self.playerOpen = ko.observable((getCookie('playerOpen') === "true"));

  self.clear = function() {
    self.room(null);
    self.playlistTracks([]);
    self.playerOpen(false);
    self.closePlayer();
  };

  self.openPlayer = function() {
    self.playerOpen(true);
    storeCookie('playerOpen', true);
    if(self.room().currentMusic()) {
      Object.keys(playerControlWrapper).forEach(function(player) {
        if(player !== self.room().currentMusic().source()) {
          playerControlWrapper[player].stop();
        }
      });
      var options = {
        music_id: self.room().currentMusic().music_id(),
        timer_start: self.room().currentMusic().timer_start() + $('#time-left-progress-bar').attr('currentTimePast'),
      };
      playerControlWrapper[self.room().currentMusic().source()].play(options);
    }
  };

  self.closePlayer = function() {
    self.playerOpen(false);
    storeCookie('playerOpen', false);
    if($('#tab_btn_playlist').hasClass('active')) {
      $('#tab_btn_playlist, #playlist').removeClass('active');
      $('#tab_btn_library, #library').addClass('active');
    }
    Object.keys(playerControlWrapper).forEach(function(player) {
      playerControlWrapper[player].stop();
    });
  };

  self.getRoom = function() {
    $.getJSON("/room", function(allData) {
      self.room(new Room(allData));
      if(self.room().currentMusic()) {
        updateProgressBar(self.room().currentMusic().duration(), self.room().current_time_past(), self.room().current_time_past_percent(), self.room().current_time_left());
      }
      else {
        stopProgressBar();
      }
    }).fail(function(jqxhr) {
      console.error(jqxhr.responseText);
    });
  };

  self.getPlaylist = function() {
    $.getJSON("/playlist", function(allData) {
      var mappedPlaylistTracks = $.map(allData, function(item) {
        return new PlaylistTrack(item);
      });
      self.playlistTracks(mappedPlaylistTracks);
    }).fail(function(jqxhr) {
      console.error(jqxhr.responseText);
    });
  };

  self.patchShuffle = function() {
    self.room().shuffle(!self.room().shuffle());
    $.ajax({
      url: '/room',
      data: ko.toJSON({shuffle: self.room().shuffle}),
      type: 'patch',
      contentType: 'application/json',
      dataType: 'json',
      success: function(allData) {
        self.room(new Room(allData));
        if(self.room().shuffle()) {
          modalConfirm($('#modal-shuffle-on'));
        }
        else {
          modalConfirm($('#modal-shuffle-off'));
        }
      },
      error: logErrors,
    });
  };

  self.postNext = function() {
    $.ajax("/room/next", {
      data: ko.toJSON({music_pk: self.room().currentMusic().pk()}),
      type: "post",
      contentType: "application/json",
      dataType: 'json',
      success: function(allData) {
        self.room(new Room(allData));
        modalConfirm($('#modal-next-music'));
      },
      error: logErrors,
    });
  };

  self.postPlaylistSort = function(pk, action, target) {
    target = (typeof target === 'undefined') ? '' : target;
    $('.overlay-playlist').show();
    var url = '/playlist';
    url += pk ? '/' + pk : '';
    url += action ? '/' + action : '';
    url += target ? '/' + target : '';
    $.ajax({
      url: url,
      type: 'post',
      contentType: 'application/json',
      dataType: 'json',
      success: function() {
        $('.overlay-playlist').hide();
      },
      error: logErrors,
    });
  };

  self.deleteMusic = function(music) {
    var pk = music ? music.pk() : self.room().currentMusic().pk();

    $.ajax("/music/" + pk, {
      type: "delete",
      contentType: "application/json",
      dataType: 'json',
      success: function() {
        musicsLibraryVM.musicsLibrary.remove(music);
        modalConfirm($('#modal-delete-music'));
      },
      error: logErrors,
    });
  };

  self.deletePlaylistTrack = function(playlistTrack) {
    self.playlistTracks.remove(playlistTrack);
    $.ajax("/playlist/" + playlistTrack.pk(), {
      type: "delete",
      contentType: "application/json",
      dataType: 'json',
      success: function() {
        modalConfirm($('#modal-delete-playlistTrack'));
      },
      error: logErrors,
    });
  };

  self.init = function() {
    self.getRoom();
    self.getPlaylist();
  };
}

// Login viewModel
function LoginViewModel() {
  var self = this;

  self.isConnected = ko.observable(false);
  self.wsConnected = ko.observable(false);
  self.wsError = ko.observable(false);
  self.badLogin = ko.observable(false);

  self.rooms = ko.observableArray([]);

  self.password = ko.observable().trimmed();
  self.selectedRoom = ko.observable();

  self.getRooms = function() {
    $.getJSON("/rooms", function(allData) {
      var mappedRooms = $.map(allData.results, function(item) {
        return new Room(item);
      });
      self.rooms(mappedRooms);
    }).fail(function(jqxhr) {
      console.error(jqxhr.responseText);
    });
  };

  self.getLogin = function() {
    if(self.password() && self.selectedRoom()) {
      $.getJSON("/login",
      {
        "name": self.selectedRoom(),
        "password": self.password()
      },
      function(allData) {
        roomVM.room(new Room(allData.room));
        self.isConnected(true);
        setRoomConnexion(allData.room.token, allData.websocket.heartbeat, allData.websocket.uri);
      }).fail(function(jqxhr) {
        self.badLogin(true);
        console.error(jqxhr.responseText);
      }
      );
    }
    else {
      self.badLogin(true);
    }
  };

  self.logOut = function() {
    self.isConnected(false);
    self.wsConnected(false);
    self.wsError(false);
    roomVM.clear();
    musicsLibraryVM.clear();
    logOutRoom();
    self.getRooms();
  };
}


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



function resize() {
  var hauteur;
  if($(window).height() > 765) {
    hauteur = $(window).height() - ($('#navbar-top').outerHeight(true) + $('footer.foot').outerHeight(true) + 25);
  }
  else {
    hauteur = 650;
  }
  // resize of the remote and the library
  $('.remote, .LIB').height(hauteur);
  $('.list-lib').height(hauteur - 90);
  $('.tab-content').height(hauteur - 130);
  $('.list-lib .panel-playlist').height(hauteur - 160);
  $('.players, .playlist-mid').height(hauteur - 250);
}


$(document).ready(function() {
  $(window).resize(function() {
    if($(window).width() > 992) {
      resize();
    }
  });
  resize();

  $('.overlay-playlist').hide();

  $('#querySearch').autocomplete({
    minLength: 2,
    source: function(request, response) {
      $.getJSON("http://suggestqueries.google.com/complete/search?callback=?",
      {
          "hl": "fr", // Language
          "ds": "yt", // Restrict lookup to youtube
          "jsonp": "suggestCallBack", // jsonp callback function name
          "q": request.term, // query term
          "client": "youtube" // force youtube style response, i.e. jsonp
        }
        );
      suggestCallBack = function(data) {
        var suggestions = [];
        if(data[1].length > 0) {
          $.each(data[1], function(key, val) {
            val[0] = val[0].substr(0, 40);
            suggestions.push({"value": val[0]});
          });
          suggestions.length = 8; // prune suggestions list to only 8 items
          response(suggestions);
        }
        else {
          $('#querySearch').autocomplete('close');
        }
      };
    },
    select: function(event, ui) {
      $(this).val(ui.item.value).change();
      $(event.target.form).submit();
    },
  });


  $(document).on({
    mouseenter: function() {
      $(this).children('.icon-trash').children('.fa-trash-o').fullOpacity();
    },
    mouseleave: function() {
      $(this).children('.icon-trash').children('.fa-trash-o').noOpacity();
    }
  }, '.playlist-item');

  $('#music_preview').on('hide.bs.modal', function() {
    Object.keys(playerPreviewControlWrapper).forEach(function(player) {
      playerPreviewControlWrapper[player].stop();
    });
  });
});


function updateVolume(volume) {
  Object.keys(playerControlWrapper).forEach(function(player) {
    storeCookie('volumePlayer', volume);
    playerControlWrapper[player].setVolume(volume);
  });
}

function displaySlider(value) {
  var offset1 = $("#slider-volume").children('.ui-slider-handle').offset();
  $(".tooltip-volume-player").css('top', offset1.top - 40).css('left', offset1.left - 5).text(value);

  var volume = $('#icon-volume');
  if(value === 0) {
    volume.css('background-position', '0 -103px');
  }
  else if(value <= 10) {
    volume.css('background-position', '0 -77px');
  }
  else if(value <= 40) {
    volume.css('background-position', '0 -52px');
  }
  else if(value <= 75) {
    volume.css('background-position', '0 -26px');
  }
  else {
    volume.css('background-position', '0 0');
  }
}

$("#slider-volume").slider({
  range: "min",
  min: 0,
  max: 100,
  create: function() {
    $("#slider-volume").slider("option", "value", getCookie('volumePlayer'));
  },
  slide: function(event, ui) {
    updateVolume(ui.value);
    displaySlider(ui.value);
  },
  change: function(event, ui) {
    updateVolume(ui.value);
    displaySlider(ui.value);
  },
  start: function() {
    $(".tooltip-volume-player").stop().fadeIn(250);
  },
  stop: function() {
    $(".tooltip-volume-player").stop().fadeOut(250);
  },
});

$("#player-wrapper").hover(
  function() {
    if($('.player-child').not('.player-child-no-music').filter(":visible").length > 0) {
      $("#wrapper-slider-volume").stop().fadeIn(300);
    }
  },
  function() {
    $("#wrapper-slider-volume").stop().fadeOut(300);
  }
  );

$('#icon-volume').click(function() {
  $("#slider-volume").slider("option", "value", 0);
});
