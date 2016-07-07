var pageSize = 40;
var reconnectTry = 0;

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

  loginVM.getRooms();
  if(getCookie('room_token')) {
    setRoomConnexion(getCookie('room_token'));
  }
  else {
    loginVM.isConnected(false);
  }
});

$(window).load(function() {
  $('.ko-login').each(function(index) {
    ko.applyBindings(loginVM, $('.ko-login')[index]);
  });
});

$(document).on('click', '.ordering-to-top, .ordering-move-up, .ordering-move-down, .ordering-to-bot', function() {
  var pk = $(this).closest("tr").data("pkplaylisttrack");
  var action = $(this).data("action");
  roomVM.postPlaylistSort(pk, action);
});

$(document).on('click', '#btn-open-player', function() {
  roomVM.openPlayer();
});


function onWsOpen() {
  reconnectTry = 0;
  loginVM.wsError(false);
  roomVM.init();
  musicsLibraryVM.init();
  loginVM.wsConnected(true);
}

function onWsError() {
  loginVM.wsError(true);
  loginVM.wsConnected(false);
}

function onWsClose() {
  loginVM.wsConnected(false);
  loginVM.logOut();
}

function wsActionUpdatePlaylistTrack(newPlaylistTracks) {
  mappedPlaylistTracks = $.map(newPlaylistTracks, function(item) {
    return new PlaylistTrack(item);
  });
  roomVM.playlistTracks(mappedPlaylistTracks);
}

function wsActionStop() {
  // Stop the players
  Object.keys(playerControlWrapper).forEach(function(player) {
    playerControlWrapper[player] && playerControlWrapper[player].stop();
    $('.player-child').not('.player-child-no-music').stop().fadeOut(250);
  });

  // Clean the room
  roomVM.room().currentMusic(null);
  roomVM.room().time_left(null);
  roomVM.room().current_time_past(null);
  roomVM.room().current_time_left(null);
  roomVM.room().current_time_past_percent(null);
  stopProgressBar();
  document.title = roomVM.room().name();
}

function wsActionShuffleChanged(message) {
  (message.shuffle) ? roomVM.room().shuffle(true) : roomVM.room().shuffle(false);
}

function wsActionMusicPatched(message) {
  music = new Music(message.music);
  music.from = 'library';

  // modify the music in the library
  var index = arrayFirstIndexOf(musicsLibraryVM.musicsLibrary(), function(item) {
    return item.pk() === music.pk();
  });
  (index >= 0) ? musicsLibraryVM.musicsLibrary()[index] = music : null;
  // notify the modification to subscribers
  musicsLibraryVM.musicsLibrary.valueHasMutated();

  // modify the musics in the playlistTracks
  ko.utils.arrayForEach(roomVM.playlistTracks(), function(item) {
    (item.music().pk() === music.pk()) ? item.music(music) : null;
  });
  // notify the modification to subscribers
  roomVM.playlistTracks.valueHasMutated();

  if(roomVM.room().currentMusic().pk() === music.pk()) {
    roomVM.room().currentMusic(music);
    roomVM.room().current_time_past($('#time-left-progress-bar').data('currentTimePast'));
    roomVM.room().current_time_left(roomVM.room().currentMusic().duration() - roomVM.room().current_time_past());
    roomVM.room().current_time_past_percent(((roomVM.room().currentMusic().duration() - roomVM.room().current_time_left()) * 100) / roomVM.room().currentMusic().duration());

    updateProgressBar(roomVM.room().currentMusic().duration(), roomVM.room().current_time_past(), roomVM.room().current_time_past_percent(), roomVM.room().current_time_left(), true);
  }
}

function wsActionMusicDeleted(message) {
  music = new Music(message.music);
  music.from = 'library';

  // remove the music in the library if it exist
  musicsLibraryVM.musicsLibrary.remove(music);

  // refresh the library
  musicsLibraryVM.getLibrary();
}

function wsActionPlay(message) {
  // Built the room
  roomVM.room().currentMusic(new Music(message.room.current_music));
  roomVM.room().count_left(message.room.count_left);
  roomVM.room().time_left(message.room.time_left);
  roomVM.room().current_time_left(message.room.current_time_left);
  roomVM.room().current_time_past(message.room.current_time_past);
  roomVM.room().current_time_past_percent(message.room.current_time_past_percent);

  // Lock the buttons
  $('.btn-to-lock').prop('disabled', true);
  setTimeout(function() {
    $('.btn-to-lock').prop('disabled', false);
  }, 1000);

  updateProgressBar(message.room.current_music.duration, message.room.current_time_past, message.room.current_time_past_percent, message.room.current_time_left);

  // Update the library
  musicsLibraryVM.getLibrary();

  // Update the playlist
  roomVM.playlistTracks.shift();

  // Update the page title
  document.title = roomVM.room().currentMusic().name();

  // Play the music
  if(roomVM.playerOpen()) {
    // stop all others players
    Object.keys(playerControlWrapper).forEach(function(player) {
      if(player !== message.room.current_music.source) {
        playerControlWrapper[player].stop();
      }
    });
    playerControlWrapper[message.room.current_music.source].play(message.room.current_music);
  }
}

function wsActionUpdateListeners(message) {
  roomVM.room().listeners(message.listeners);
}

function wsActionUpdateVolume(message) {
  // TODO
}

// receive a message though the websocket from the server
function receiveMessage(message) {
  switch(message.action) {
    case 'stop':
      wsActionStop();
      break;
    case 'shuffle_changed':
      wsActionShuffleChanged(message);
      break;
    case 'music_patched':
      wsActionMusicPatched(message);
      break;
    case 'music_deleted':
      wsActionMusicDeleted(message);
      break;
    case 'playlistTrack_updated':
      wsActionUpdatePlaylistTrack(message.playlistTracks);
      break;
    case 'playlistTrack_deleted':
      wsActionUpdatePlaylistTrack(message.playlistTracks);
      break;
    case 'music_added':
      wsActionUpdatePlaylistTrack(message.playlistTracks);
      break;
    case 'volume_changed':
      wsActionUpdateVolume(message);
      break;
    case 'play':
      wsActionPlay(message);
      break;
    case 'listeners_updated':
      wsActionUpdateListeners(message);
      break;
    default:
      console.warn("Unknow socket received : ");
      console.log(message);
      break;
  }
}
