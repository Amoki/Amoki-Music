// MODEL DEFINITION
// Music model
function Music(data) {
  this.musicId = ko.observable(data.music_id);
  this.name = ko.observable(data.name);
  url = ko.observable(data.url);
  room = ko.observable(data.room);
  date = ko.observable(data.date);
  this.duration = ko.observable(data.duration);
  this.thumbnail = ko.observable(data.thumbnail);
  this.count = ko.observable(data.count);
  lastPlay = ko.observable(data.last_play);
  deadLink = ko.observable(data.dead_link);
  timerStart = ko.observable(data.timer_start);
  timerEnd = ko.observable(data.timer_end);
  source = ko.observable(data.source);
}
// Source model
function Source(data) {
  this.name = ko.observable(data.name);
}

// VIEW MODEL DEFINITION
// Library view model
function LibraryViewModel() {
  var self = this;
  self.musicsLibrary = ko.observableArray([]);
  self.musicSearch = ko.observableArray([]);

  // TEST ONLY
  self.sources = ko.observableArray([
      new Source({name: "test"}),
      new Source({name: "test2"}),
    ]);

  self.addMusic = function(Music) {
    endpointAddMusic(Music);
  };

  self.searchMusic = function(query) {
    // Return a json serialized Music object
    $.getJSON("/search?q=" + query, function(allData) {
      var mappedMusics = $.map(allData, function(item) {
        return new Music(item);
      });
      self.musicSearch(mappedMusics);
    }).fail(function(jqxhr) {
      console.error(jqxhr.responseText);
    });
  };

  // Load Library page from server, convert it to Music instances, then populate self.musics
  self.getLibrary = function(page) {
    $.getJSON("/musics?page=" + page, function(allData) {
      var mappedMusics = $.map(allData, function(item) {
        return new Music(item);
      });
      self.musicsLibrary(mappedMusics);
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
}

// Playist view model
function PlaylistViewModel() {
  var self = this;
  self.musics = ko.observableArray([]);

  self.addMusic = function(Music) {
    endpointAddMusic(Music);
  };
  self.removeMusic = function(Music) {
    self.musics.remove(Music);
  };

  // Load Playlist from server, convert it to Music instances, then populate self.musics
  self.getPlaylist = function() {
    $.getJSON("/playlist/", function(allData) {
      var mappedMusics = $.map(allData, function(item) {
        return new Music(item);
      });
      self.musics(mappedMusics);
    }).fail(function(jqxhr) {
      console.error(jqxhr.responseText);
    });
  };
}


$(function() {
  musicsPlaylistVM = new PlaylistViewModel();
  musicsLibraryVM = new LibraryViewModel();
  // Local Binding to avoid multi binding by musicsPlaylistVM and musicsLibraryVM
  $('.ko-playlist').each(function(index) {
    ko.applyBindings(musicsPlaylistVM, $('.ko-playlist')[index]);
  });
  $('.ko-library').each(function(index) {
    ko.applyBindings(musicsLibraryVM, $('.ko-library')[index]);
  });

  // TODO Transfer to Redis onSubscribe
  musicsPlaylistVM.getPlaylist();
  // musicsLibraryVM.getLibrary(1);
});
