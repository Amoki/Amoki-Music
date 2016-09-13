// VIEW MODEL DEFINITION
// Library view model
function LibraryViewModel() {
  var self = this;

  // library part
  self.musicsLibrary = ko.observableArray([]);
  self.hasPrevious = ko.observable();
  self.hasNext = ko.observable();
  self.currentPage = ko.observable(1);

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
    self.currentPage(1);
    self.musicSearch([]);
    self.sourceSearch(null);
    self.querySearch(null);
    self.sources([]);
    self.musicPreview(null);
  };

  self.addMusic = function(music, oneShot) {
    // Return a json serialized Music object
    music.one_shot = oneShot;
    $.ajax("/music", {
      data: ko.toJSON(music),
      type: "post",
      contentType: "application/json",
      dataType: "json",
      success: function() {
        $("button.btn-add-music").removeClass("icon-refresh").children("span").attr("class", "glyphicon glyphicon-play-circle");
        $("button.btn-add-music").prop('disabled', false);
        $("button.btn-add-music-one-shot").removeClass("icon-refresh").children("span").attr("class", "glyphicon glyphicon-fire");
        $("button.btn-add-music-one-shot").prop('disabled', false);
        modalConfirm($('#modal-add-music'));
      },
      error: logErrors,
    });
  };

  self.patchMusic = function(music, play) {
    // Return a json serialized Music object
    $.ajax("/music", {
      data: ko.toJSON(music),
      type: "patch",
      contentType: "application/json",
      dataType: "json",
      success: function() {
        if(!play) {
          $("button.btn-add-music").removeClass("icon-refresh").children("span").attr("class", "glyphicon glyphicon-play-circle");
          $("button.btn-add-music").prop('disabled', false);
          $("button.btn-add-music-one-shot").removeClass("icon-refresh").children("span").attr("class", "glyphicon glyphicon-fire");
          $("button.btn-add-music-one-shot").prop('disabled', false);
          modalConfirm($('#modal-add-music'));
        }
        else {
          self.addMusic(music,false);
        }
      },
      error: logErrors,
    });
  };

  self.sendMusic = function(music, play, oneShot) {
    $("button.btn-add-music").addClass("icon-refresh").children("span").attr("class", "fa fa-refresh fa-spin");
    $("button.btn-add-music").prop('disabled', true);
    $("button.btn-add-music-one-shot").addClass("icon-refresh").children("span").attr("class", "fa fa-refresh fa-spin");
    $("button.btn-add-music-one-shot").prop('disabled', true);
    if(music.from === 'search') {
      self.addMusic(music, oneShot);
    }
    else if(music.from === 'library') {
      (play === 'play') ? self.addMusic(music,false) : self.patchMusic(music, play);
    }
  };

  self.openPreviewMusic = function(music) {
    updateVolume(0, true);
    self.musicPreview(music);
    handlerStart = self.musicPreview().timer_start() ? self.musicPreview().timer_start() : 0;
    handlerEnd = self.musicPreview().timer_end() ? self.musicPreview().timer_end() : self.musicPreview().total_duration();
    customSlider.slide({
      element: $("#slider-preview"),
      max: self.musicPreview().total_duration(),
      values: [handlerStart, handlerEnd],
      currentPlayerControl: playerPreviewControlWrapper[music.source()],
    });
    playerPreviewControlWrapper[music.source()].play({music_id: self.musicPreview().music_id()});
  };

  self.closePreviewMusic = function(valid, play, oneShot) {
    updateVolume(getCookie('volumePlayer'), true);
    $('#music_preview').modal('hide');
    if(valid) {
      self.musicPreview().timer_start($('#slider-preview').slider("values", 0));
      self.musicPreview().duration(self.musicPreview().total_duration() - self.musicPreview().timer_start() - (self.musicPreview().total_duration() - $('#slider-preview').slider("values", 1)));
      self.sendMusic(self.musicPreview(), play, oneShot);
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
      $("#popover-container-custom").scrollTop(0);
      $("button.btn-search-icon").children("i").attr("class", "fa fa-search");
      $("button.btn-search-icon").prop('disabled', false);
    }).fail(function(jqxhr) {
      console.error(jqxhr.responseText);
    });
  };

  // Load Library page from server, convert it to Music instances, then populate self.musics
  self.getLibrary = function(target, event) {
    url = event ? event.target.value : url = "/musics?page=" + self.currentPage() + "&page_size=" + pageSize;
    $.getJSON(url, function(allData) {
      var mappedMusics = $.map(allData.results, function(item) {
        item.from = 'library';
        return new Music(item);
      });
      self.musicsLibrary(mappedMusics);
      self.hasPrevious(allData.previous);
      self.hasNext(allData.next);
      event ? ($(event.currentTarget).data('action') === "getNextPage" ? self.currentPage(self.currentPage() + 1) : self.currentPage(self.currentPage() - 1)) : null ;
      event ? $("#popover-container-custom").scrollTop(0) : null;
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
      timePast = ($('#time-left-progress-bar').data('currentTimePast') ? $('#time-left-progress-bar').data('currentTimePast') : self.room().current_time_past());
      var options = {
        music_id: self.room().currentMusic().music_id(),
        timer_start: self.room().currentMusic().timer_start() + timePast,
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
        document.title = self.room().currentMusic().name();
      }
      else {
        stopProgressBar();
        document.title = self.room().name();
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
    $('#submit-shuffle').prop('disabled', true);
    self.room().shuffle(!self.room().shuffle());
    $.ajax({
      url: '/room',
      data: ko.toJSON({shuffle: self.room().shuffle}),
      type: 'patch',
      contentType: 'application/json',
      dataType: 'json',
      success: function() {
        $('#submit-shuffle').prop('disabled', false);
        (self.room().shuffle()) ? modalConfirm($('#modal-shuffle-on')) : modalConfirm($('#modal-shuffle-off'));
      },
      error: logErrors,
    });
  };

  self.postNext = function() {
    $('.btn-to-lock').prop('disabled', true);
    $.ajax("/room/next", {
      data: ko.toJSON({music_pk: self.room().currentMusic().pk()}),
      type: "post",
      contentType: "application/json",
      dataType: 'json',
      success: function() {
        modalConfirm($('#modal-next-music'));
      },
      error: logErrors,
    });
  };

  self.postPlaylistSort = function(pk, action, target) {
    $('.overlay-playlist').show();
    var data = {
      'pk': pk,
      'action' : action,
      'target' : target
    };
    data = ko.toJSON(data);
    $.ajax({
      url: '/playlist',
      type: 'post',
      contentType: 'application/json',
      dataType: 'json',
      data: data,
      success: function() {
        $('.overlay-playlist').hide();
      },
      error: logErrors,
    });
  };

  self.deleteMusic = function(music) {
    pk = music ? music.pk() : self.room().currentMusic().pk();

    $.ajax("/music", {
      type: "delete",
      contentType: "application/json",
      dataType: 'json',
      data: ko.toJSON({'pk': pk}),
      success: function() {
        modalConfirm($('#modal-delete-music'));
      },
      error: logErrors,
    });
  };

  self.deletePlaylistTrack = function(playlistTrack) {
    self.playlistTracks.remove(playlistTrack);
    $.ajax("/playlist", {
      type: "delete",
      contentType: "application/json",
      dataType: 'json',
      data: ko.toJSON({pk: playlistTrack.pk()}),
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
