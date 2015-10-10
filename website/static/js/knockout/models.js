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
