function updatePlayer() {
  $.ajax({
    type: "POST",
    url: "/update-player/",
    data: {},
    dataType: "json",
    success: function(data) {
      $('.playlist-ajax').html(data.template_playlist);
      if(data.current_music) {
        $("#dead-link").removeAttr('disabled');
        $('#music_id-dead-link').val(data.current_music[0].fields.music_id);
      }
      else {
        $("#dead-link").attr('disabled', 'disabled');
      }
    },
    error: logErrors
  });
}
