$( document ).ready(function() {
  $('#time-left-progress-bar').countdown('destroy');

  $.countdown.setDefaults({
    compact: true,
    onExpiry: update_player,
  });
});


function timeline(current_time_left, current_time_past_percent){
  $(".progress-bar").stop();
  var actual_time = current_time_left;
  actual_time *= 1000;
  $(".progress-bar").css('width', current_time_past_percent+'%');
  $(".progress-bar").animate({ 'width' : '100%'} , {
      duration: actual_time,
      easing: 'linear',
  });
}
