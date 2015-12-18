var pageSize = 40;

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

  loginVM.getRooms();
  if(getCookie('room_token') && getCookie('room_heartbeat') && getCookie('room_wsUri')) {
    setRoomConnexion(getCookie('room_token'), getCookie('room_heartbeat'), getCookie('room_wsUri'));
  }
  else {
    loginVM.isConnected(false);
  }
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
  loginVM.wsError(false);
  loginVM.isConnected(true);
  roomVM.init();
  musicsLibraryVM.init();
}

function onWsError() {
  loginVM.wsError(true);
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
    playerControlWrapper[player].stop();
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
  url = "/musics?page=" + musicsLibraryVM.currentPage() + "&page_size=" + pageSize;
  $.getJSON(url, function(allData) {
    var mappedMusics = $.map(allData.results, function(item) {
      item.from = 'library';
      return new Music(item);
    });
    musicsLibraryVM.musicsLibrary(mappedMusics);
    musicsLibraryVM.hasPrevious(allData.previous);
    musicsLibraryVM.hasNext(allData.next);
  }).fail(function(jqxhr) {
    console.error(jqxhr.responseText);
  });
}

function wsActionPlay(message) {
  // Built the room
  room = new Room(message.room);

  // Update the room
  roomVM.room(room);
  updateProgressBar(message.room.current_music.duration, message.room.current_time_past, message.room.current_time_past_percent, message.room.current_time_left);

  // Update the library
  musicExtracted = musicsLibraryVM.musicsLibrary.remove(function(item) {
    return item.pk() === message.room.current_music.pk;
  });
  if(musicExtracted.length > 0) {
    musicsLibraryVM.musicsLibrary.unshift(musicExtracted[0]);
  }
  else {
    musicsLibraryVM.musicsLibrary.unshift(new Music(message.room.current_music));
    musicsLibraryVM.musicsLibrary.pop();
  }
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


