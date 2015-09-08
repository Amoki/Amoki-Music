
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

function MusicsPlaylist() {
  var self = this;
  self.musics = ko.observableArray([]);

  this.print = function() {
    alert(ko.toJSON(self.musics));
  };

  // addMusic (to playlist)
  self.addMusic = function(Music) {
    self.musics.push(Music);
    // TODO call endpoint POST /music
    $.ajax("/music", {
      data: ko.toJSON({musics: self.musics}),
      type: "post", contentType: "application/json",
      success: function(result) {
        alert(result);
      }
    });
  };

  // Load Playlist from server, convert it to Music instances, then populate self.musics
  self.getPlaylist = function() {
    $.getJSON("/playlist", function(allData) {
      var mappedMusics = $.map(allData, function(item) {
        return new Music(item);
      });
      self.musics(mappedMusics);
    }).fail(function(jqxhr) {
      console.error(jqxhr.responseText);
    });
  };
}

function MusicsLibrary() {
  var self = this;
  self.musics = ko.observableArray([]);

  self.addMusic = function(Music) {
    self.musics.push(Music);
    // TODO call endpoint POST /music
    $.ajax("/music", {
      data: ko.toJSON({musics: self.musics}),
      type: "post", contentType: "application/json",
      success: function(result) {
        alert(result);
      }
    });
  };
  self.removeMusic = function(Music) {
    self.musics.destroy(Music);
    // TODO call endopoint  DELETE /music
  };

  // Load Library from server, convert it to Music instances, then populate self.musics
  self.getLibrary = function(page) {
    $.getJSON("/musics?page=" + page, function(allData) {
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
  musicsPlaylistVM = new MusicsPlaylist();
  musicsLibraryVM = new MusicsLibrary();
  // Local Binding to avoid multi binding by musicsPlaylistVM and musicsLibraryVM
  $('.playlist-ko').each(function(index) {
    ko.applyBindings(musicsPlaylistVM, $('.playlist-ko')[index]);
  });
  // ko.applyBindings(musicsLibraryVM);

  // TODO Transfer to Redis onSubscribe
  musicsPlaylistVM.getPlaylist();
  // musicsLibraryVM.getLibrary(1);
});
