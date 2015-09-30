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
// Playlist model
function PlaylistTrack(data) {
  this.pk = ko.observable(data.pk);
  this.order = ko.observable(data.order);
  this.music = ko.observable(new Music(data.music));
}
// Room model
function Room(data) {
  this.name = ko.observable(data.name);
  this.time_left = ko.observable(data.time_left);
  this.current_time_left = ko.observable(data.current_time_left);
  this.current_time_past = ko.observable(data.current_time_past);
  this.current_time_past_percent = ko.observable(data.current_time_past_percent);
  this.can_adjust_volume = ko.observable(data.can_adjust_volume);
  this.shuffle = ko.observable(data.shuffle);
  this.count_left = ko.observable(data.count_left);

  this.currentMusic = ko.observable();
  if(data.current_music) {
    this.currentMusic = new Music(data.current_music);
  }
  else {
    this.currentMusic = null;
  }
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

  self.addMusic = function() {
    $("button.btn-add-music").children("span").attr("class", "fa fa-2x fa-refresh fa-spin");
    $("button.btn-add-music").attr('disabled', 'disabled');
    // Return a json serialized Music object
    $.ajax("/music", {
      data: ko.toJSON(this),
      type: "post",
      contentType: "application/json",
      dataType: "json",
      success: function(result) {
        newMusic = new Music(result);
        $("button.btn-add-music").children("span").attr("class", "glyphicon glyphicon-play-circle");
        $("button.btn-add-music").removeAttr('disabled');
      }
    });
  };

  self.searchMusic = function() {
    // Return a json serialized Music object
    if($.type(ko.toJS(self.querySearch)) === "undefined" || !self.querySearch()) {
      // TODO Display empty field warning
      return;
    }
    $("button.btn-search-icon").children("i").attr("class", "fa fa-refresh fa-spin");
    $("button.btn-search-icon").attr('disabled', 'disabled');
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
        $("button.btn-search-icon").children("i").attr("class", "fa fa-search");
        $("button.btn-search-icon").removeAttr('disabled');
      }).fail(function(jqxhr) {
        console.error(jqxhr.responseText);
      });
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

  self.getRoom = function() {
    $.getJSON("/room", function(allData) {
      self.room(new Room(allData));
      if(self.room().currentMusic) {
        updateProgressBar(self.room().currentMusic.duration(), self.room().current_time_past(), self.room().current_time_left());
        timeline(self.room().current_time_left(), self.room().current_time_past_percent());
      }
      else {
        stopAll();
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

  self.postPlaylistSort = function(pk, action, target) {
    target = (typeof target === 'undefined') ? '' : target;
    $('#overlay-playlist').show();
    $.ajax({
      url: '/playlist/' + pk + '/' + action + '/' + target,
      type: 'post',
      contentType: 'application/json',
      dataType: 'json',
      success: function(allData) {
        $('#overlay-playlist').hide();
        console.log(allData);
      },
      error: logErrors,
    });
  };

  self.deleteMusic = function() {
    $.ajax("/music/" + self.room().currentMusic.pk(), {
      type: "delete",
      contentType: "application/json",
      dataType: 'json',
      success: function(allData) {
        console.log(allData);
      },
      error: logErrors,
    });
  };

  self.deletePlaylistTrack = function() {
    $.ajax("/?/", {
      type: "delete",
      contentType: "application/json",
      dataType: 'json',
      success: function(allData) {
        console.log(allData);
      },
      error: logErrors,
    });
  };
}

// Login viewModel
function LoginViewModel() {
  var self = this;

  self.isConnected = ko.observable(false);

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

$(document).on('click', '.ordering-to-top, .ordering-move-up, .ordering-move-down, .ordering-to-bot', function() {
  var pk = $(this).closest("tr").attr("id");
  var action = $(this).data("action");
  roomVM.postPlaylistSort(pk, action);
});

var sortableOptions = {
  axis: "y",
  containment: ".panel-playlist",
  revert: true,
  cursor: "move",
  scrollSpeed: 5,
  delay: 250,
  over: function() {
    $(this).find('.ui-sortable-helper').appendTo(this);
  },
};

function onWsOpen() {
  loginVM.isConnected(true);
  roomVM.getRoom();
  roomVM.getPlaylist();
  musicsLibraryVM.init();
}

// receive a message though the websocket from the server
function receiveMessage(message) {
  message = JSON.parse(message);
  if(message.update === true) {
    roomVM.getRoom();
    roomVM.getPlaylist();
    musicsLibraryVM.getLibrary();
  }
}

ko.bindingHandlers.stopBinding = {
  init: function() {
    return {controlsDescendantBindings: true};
  }
};

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
        isDisabled = selectPickerOptions.disabledCondition || false,
        resetOnDisabled = selectPickerOptions.resetOnDisabled || false;
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
