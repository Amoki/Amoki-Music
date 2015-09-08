
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

  self.addMusic = function(Music) {
    self.musics.push(Music);
    // TODO call endpoint DELETE /music
  };
  self.removeMusic = function(Music) {
    self.musics.destroy(Music);
    // TODO call endopoint POST /music
  };
  this.print = function() {
    alert(ko.toJSON(self.musics));
  };

  // Load Playlist state from server, convert it to Music instances, then populate self.musics
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

$(function() {
  musicsPlaylistVM = new MusicsPlaylist();
  ko.applyBindings(musicsPlaylistVM);

  // TODO Transfer to Redis onSubscribe
  musicsPlaylistVM.getPlaylist();
});

