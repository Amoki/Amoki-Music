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
  this.one_shot = ko.observable(data.one_shot);

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
  this.listeners = ko.observable(data.listeners);
}
// Source model
function Source(data) {
  this.name = ko.observable(data.capitalize());
}
