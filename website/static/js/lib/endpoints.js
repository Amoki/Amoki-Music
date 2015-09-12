function endpointAddMusic(newMusic) {
  // Return a json serialized Music object
  $.ajax("/music", {
    data: ko.toJSON({music: newMusic}),
    type: "post",
    contentType: "application/json",
    dataType: "json",
    success: function(result) {
      newMusic = new Music(result);
      musicsPlaylistVM.musics.push(newMusic);
      musicsLibraryVM.musicsLibrary.push(newMusic);
    }
  });
}
