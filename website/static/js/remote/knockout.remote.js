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


function onWsOpen() {
  loginVM.wsError(false);
  loginVM.isConnected(true);
  roomVM.init();
  musicsLibraryVM.init();
}

function onWsError() {
  loginVM.wsError(true);
}


function updatePlaylistTrack(newPlaylistTracks) {
  mappedPlaylistTracks = $.map(newPlaylistTracks, function(item) {
    return new PlaylistTrack(item);
  });
  roomVM.playlistTracks(mappedPlaylistTracks);
}

// receive a message though the websocket from the server
function receiveMessage(message) {
  switch(message.action) {
    case 'stop':
      // Stop the players
      Object.keys(playerControlWrapper).forEach(function(player) {
        playerControlWrapper[player].stop();
        $('.player-child').not('.player-child-no-music').stop().fadeOut(250);
      });

      // Clean the room
      roomVM.room().current_music(null);
      roomVM.room().time_left(null);
      roomVM.room().current_time_past(null);
      roomVM.room().current_time_left(null);
      roomVM.room().current_time_past_percent(null);
      stopProgressBar();

      break;
    case 'shuffle_changed':
      if(message.shuffle) {
        roomVM.room().shuffle(true);
      }
      else {
        roomVM.room().shuffle(false);
      }
      break;
    case 'music_patched':
      music = new Music(message.music);
      music.from = 'library';

      // modify the music in the library
      musicsLibraryVM.musicsLibrary()[arrayFirstIndexOf(musicsLibraryVM.musicsLibrary(), function(item) {
        return item.pk() === music.pk();
      })] = music;
      // notify the modification to ²
      musicsLibraryVM.musicsLibrary.valueHasMutated();

      break;
    case 'music_deleted':
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

      break;
    case 'playlistTrack_updated':
      updatePlaylistTrack(message.playlistTracks);
      break;
    case 'playlistTrack_deleted':
      updatePlaylistTrack(message.playlistTracks);
      break;
    case 'music_added':
      updatePlaylistTrack(message.playlistTracks);
      break;
    case 'volume_changed':
      // TODO
      break;
    case 'play':
      // Built the room
      room = new Room(message.room);

      // Update the room
      roomVM.room(room);
      message.room.current_music ? updateProgressBar(message.room.current_music.duration, message.room.current_time_past, message.room.current_time_past_percent, message.room.current_time_left) : stopProgressBar();

      // Update the library
      musicsLibraryVM.musicsLibrary.remove(function(item) {
        return item.pk() === message.room.current_music.pk;
      });
      musicsLibraryVM.musicsLibrary.unshift(roomVM.room().currentMusic());
      musicsLibraryVM.musicsLibrary.pop();

      // Update the playlist
      roomVM.playlistTracks.shift();

      if(roomVM.playerOpen()) {
        // stop all others players
        Object.keys(playerControlWrapper).forEach(function(player) {
          if(player !== message.room.current_music.source) {
            playerControlWrapper[player].stop();
          }
        });
        playerControlWrapper[message.room.current_music.source].play(message.room.current_music);
      }
      break;
    case 'listeners_updated':
      roomVM.room().listeners(message.listeners);
      break;
    default:
      console.warn("Unknow socket received : ");
      console.log(message);
      break;
  }

  if(message.update === true) {
    roomVM.getRoom();
    roomVM.getPlaylist();
    musicsLibraryVM.getLibrary();
  }
}

$(document).on('click', '#btn-open-player', function() {
  roomVM.openPlayer();
});
