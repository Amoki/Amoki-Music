function updatePlayer() {
  $.ajax({
    type: "POST",
    url: "/update-player/",
    data: {},
    dataType: "json",
    success: function(data) {
      $('.playlist-ajax').html(data.templatePlaylist);
      if(data.currentMusic) {
        $("#dead-link").removeAttr('disabled');
        $('#music_id-dead-link').val(data.currentMusic.music_id);
      }
      else {
        $("#dead-link").attr('disabled', 'disabled');
      }
    },
    error: logErrors
  });
}
