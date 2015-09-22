var pageSize = 40;

// MODEL DEFINITION
// Music model
function Music(data) {
  this.pk = ko.observable(data.pk);
  this.music_id = ko.observable(data.music_id);
  this.name = ko.observable(data.name);
  this.url = ko.observable(data.url);
  this.room = ko.observable(data.room);
  this.date = ko.observable(data.date);
  this.duration = ko.observable(data.duration);
  this.thumbnail = ko.observable(data.thumbnail);
  this.count = ko.observable(data.count || data.views);
  this.last_play = ko.observable(data.last_play);
  this.dead_link = ko.observable(data.dead_link);
  this.timer_start = ko.observable(data.timer_start);
  this.timer_end = ko.observable(data.timer_end);
  this.source = ko.observable(data.source);
}
// Room model
function Room(data) {
  this.name = ko.observable(data.name);
  this.timeLeft = ko.observable(data.time_left);
  this.currentTimeLeft = ko.observable(data.current_time_left);
  this.canAdjustVolume = ko.observable(data.can_adjust_volume);
  this.shuffle = ko.observable(data.shuffle);
  this.countLeft = ko.observable(data.count_left);

  this.currentMusic = ko.observableArray([]);
  if(data.current_music) {
    this.currentMusic = new Music(data.current_music);
  }
  else {
    this.currentMusic = null;
  }

  this.playlist = ko.observableArray([]);
  var mappedMusics = $.map(data.playlist, function(item) {
    return new Music(item);
  });
  this.playlist(mappedMusics);
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

  // TEST ONLY
  self.sources = ko.observableArray([]);

  self.addMusic = function() {
    // Return a json serialized Music object
    $.ajax("/music", {
      data: ko.toJSON(this),
      type: "post",
      contentType: "application/json",
      dataType: "json",
      success: function(result) {
        newMusic = new Music(result);
      }
    });
  };

  self.searchMusic = function() {
    // Return a json serialized Music object
    if($.type(ko.toJS(self.querySearch)) === "undefined" || !ko.toJS(self.querySearch).trim()) {
      // TODO Display empty field warning
      console.log("empty");
      return;
    }
    $.getJSON("/search",
      {
        "service": ko.toJS(self.sourceSearch).toLowerCase(),
        "query": self.querySearch()
      },
      function(allData) {
        var mappedMusics = $.map(allData, function(item) {
          return new Music(item);
        });
        self.musicSearch(mappedMusics);
        $("#tab_btn_library, #library").removeClass('active');
        $("#tab_btn_search, #search-tab").addClass('active');
      }).fail(function(jqxhr) {
        console.error(jqxhr.responseText);
      });
  };

  self.getOptions = function(request, response) {
    $.getJSON("http://suggestqueries.google.com/complete/search?callback=?",
      {
        "hl": "fr", // Language
        "ds": "yt", // Restrict lookup to youtube
        "jsonp": "suggestCallBack", // jsonp callback function name
        "q": request, // query term
        "client": "youtube" // force youtube style response, i.e. jsonp
      }
    );
    suggestCallBack = function(data) {
      var suggestions = [];
      $.each(data[1], function(key, val) {
        val[0] = val[0].substr(0, 40);
        suggestions.push({"value": val[0]});
      });
      suggestions.length = 8; // prune suggestions list to only 8 items
      response(suggestions);
    };
  };

  // Load Library page from server, convert it to Music instances, then populate self.musics
  self.getLibrary = function(target, event) {
    event ? url = event.target.value : url = "/musics?page_size=" + pageSize;
    $.getJSON(url,
      function(allData) {
        var mappedMusics = $.map(allData.results, function(item) {
          return new Music(item);
        });
        self.musicsLibrary(mappedMusics);
        self.hasPrevious(allData.previous);
        self.hasNext(allData.next);
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
  self.musicsPlaylist = ko.observableArray([]);

  self.getRoom = function() {
    $.getJSON("/room", function(allData) {
      self.room(new Room(allData));
    }).fail(function(jqxhr) {
      console.error(jqxhr.responseText);
    });
  };

  self.patchShuffle = function() {
    self.room().shuffle = !self.room().shuffle();
    $.ajax({
      url: '/room',
      data: ko.toJSON({shuffle: self.room().shuffle}),
      type: 'patch',
      contentType: 'application/json',
      dataType: 'json',
      success: function(allData) {
        self.room(new Room(allData));
      },
      error: logErrors,
    });
  };

  self.postNext = function() {
    $.ajax("/room/next", {
      data: ko.toJSON({music_pk: self.room().currentMusic.pk()}),
      type: "post",
      contentType: "application/json",
      dataType: 'json',
      success: function(allData) {
        self.room(new Room(allData));
      },
      error: logErrors,
    });
  };
}

// Login viewModel
function LoginViewModel() {
  var self = this;

  self.isConnected = ko.observable();

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
          setRoomConnexion(allData.room.token, allData.websocket.heartbeat, allData.websocket.uri);
        }).fail(function(jqxhr) {
          console.error(jqxhr.responseText);
        }
      );
    }
    else {
      console.log("no pass");
      // TODO Front bad password
      return;
    }
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
  musicsLibraryVM.init();
}

ko.bindingHandlers.stopBinding = {
  init: function() {
    return {controlsDescendantBindings: true};
  }
};

ko.subscribable.fn.trimmed = function() {
  return ko.computed({
    read: function() {
      if(this()) {
        return this().trim();
      }
      else {
        return this();
      }
    },
    write: function(value) {
      this(value.trim());
      this.valueHasMutated();
    },
    owner: this
  });
};
