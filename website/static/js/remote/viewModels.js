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
    $("button.btn-add-music").addClass("icon-refresh").children("span").attr("class", "fa fa-refresh fa-spin");
    $("button.btn-add-music").prop('disabled', true);
    // Return a json serialized Music object
    $.ajax("/music", {
      data: ko.toJSON(music),
      type: "post",
      contentType: "application/json",
      dataType: "json",
      success: function(result) {
        newMusic = new Music(result);
        $("button.btn-add-music").removeClass("icon-refresh").children("span").attr("class", "glyphicon glyphicon-play-circle");
        $("button.btn-add-music").prop('disabled', false);
        modalConfirm($('#modal-add-music'));
      }
    });
  };

  self.openPreviewMusic = function(music) {
    self.musicPreview(music);
    customSlider.slide({
      element: $("#slider-preview"),
      max: self.musicPreview().duration(),
      values: [0, self.musicPreview().duration()],
      currentPlayerControl: playerPreviewControlWrapper[music.source()],
    });
    playerPreviewControlWrapper[music.source()].play({music_id: self.musicPreview().music_id()});
  };

  self.closePreviewMusic = function(valid) {
    $('#music_preview').modal('hide');
    if(valid) {
      self.musicPreview().timer_start($('#slider-preview').slider("values", 0));
      self.musicPreview().timer_end($('#slider-preview').slider("values", 1));
      self.addMusic(self.musicPreview());
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
    event ? url = event.target.value : url = "/musics?page_size=" + pageSize;
    $.getJSON(url, function(allData) {
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

  (!Cookies.get('playerOpen') || Cookies.get('playerOpen') === false) ? Cookies.set('playerOpen', false) : null;
  self.playerOpen = ko.observable((Cookies.get('playerOpen') === "true"));

  self.clear = function() {
    self.room(null);
    self.playlistTracks([]);
    self.playerOpen(false);
    self.closePlayer();
  };

  self.openPlayer = function() {
    self.playerOpen(true);
    Cookies.set('playerOpen', true);
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
    Cookies.set('playerOpen', false);
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
    pk = music ? music.pk() : self.room().currentMusic().pk();

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
}

// Login viewModel
function LoginViewModel() {
  var self = this;

  self.isConnected = ko.observable(false);
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
    roomVM.clear();
    musicsLibraryVM.clear();
    logOutRoom();
    self.getRooms();
  };
}
