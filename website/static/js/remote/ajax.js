var currentPage = 0;

$(document).on('submit', '.ajax-shuffle', function(e) {
  e.preventDefault();
  var $this = $(this);
  ajax($this).done(function(data) {
    if(data.error) {
      modalConfirm($('#modal-shuffle-error'));
    }
    else if(data.shuffle === true) {
      modalConfirm($('#modal-shuffle-on'));
    }
    else {
      modalConfirm($('#modal-shuffle-off'));
    }
  })
  .fail(logErrors);
});

$(document).on('change', 'select#source', function() {
  $('.ajax-search').submit();
});

$(document).on('submit', '.ajax-search', function(e) {
  e.preventDefault();
  var $this = $(this);
  var source = $this.find('#input-source-selected').val().toLowerCase();
  if($this.find('input#query').val().trim() === '' || $this.find('input#query').val().trim() === null) {
    $("#list-" + source).slideUp();
    $("#list-" + source).promise().done(function() {
      $("#list-" + source).children().remove();
      $("#list-" + source).append('<li class="list-group-item item-lib ' + source + '-list-music"><div class="row"><p class="col-xs-10">Enter your search in the field above</p><i class="fa fa-level-up fa-2x col-xs-2"></i></div></li>');
      $("#list-" + source).slideDown();
    });
    return;
  }

  ajax($this).done(function(data) {
    if(data.currentMusic) {
      $("input#query").removeAttr('disabled');
      modalConfirm($('#modal-add-music'));
    }
    else {
      $(".list-lib .nav-tabs").find("li").removeClass("active");
      $(".tab-content").find(".tab-pane").removeClass("active");
      $("#tab_btn_" + source).addClass("active");
      $("#" + source).addClass("active");
      $("#list-" + source).slideUp();
      $("#list-" + source).promise().done(function() {
        $("." + source + "-list-music").remove();
        $("#list-" + source).html(data.templateLibrary);
        $("#list-" + source).slideDown();
        $("#list-" + source).promise().done(function() {});
      });
    }
  })
  .fail(logErrors);
});

$(document).on('submit', '.ajax-add-music', function(e) {
  e.preventDefault();
  var $this =  $(this);
  $this.children("button").children("span").attr("class", "fa fa-refresh fa-spin");
  $this.children("button").attr('disabled', 'disabled');

  ajax($this).done(function() {
    $this.children("button").children("span").attr('class', 'glyphicon glyphicon-headphones');
    $this.children("button").removeAttr('disabled');
    modalConfirm($('#modal-add-music'));
  })
  .fail(logErrors);
});

$(document).on('submit', '.ajax-volume', function(e) {
  e.preventDefault();
  var $this = $(this);

  ajax($this).done(function() {
    $this.children(".volume_clicked").removeClass("volume_clicked");
  })
  .fail(logErrors);
});

$(document).on('submit', '.ajax_music_infinite_scroll', function(e) {
  e.preventDefault();
  var $this = $(this);
  $("<li id='spinner_library' class='list-group-item item-lib row row-list-item' style='color:black'><i class='fa fa-spinner fa-4x fa-spin'></i></li>").insertBefore($this.closest('li'));

  ajax($this).done(function(data) {
    $(data.template).insertBefore($this.closest('li'));
    if(data.moreMusics === false) {
      $this.children("#load-more-musics").addClass('disabled');
    }
    currentPage += 1;
    $("#page").val(currentPage);
    $("#spinner_library").remove();
  })
  .fail(logErrors);
});

function updateRemote(action) {
  var dataSend = {
      'page': encodeURIComponent($('.ajax_music_infinite_scroll').children("#page").val()),
    };
  $.ajax({
    type: "POST",
    url: "/update-remote/",
    data: dataSend,
    dataType: "json",
    success: function(data) {
      if(data.shuffle === true) {
        $("#btn-shuffle").attr("value", "false");
        $("#submit-shuffle").attr("class", "btn btn-default btn-control btn-shuffle-true");
      }
      else {
        $("#btn-shuffle").attr("value", "true");
        $("#submit-shuffle").attr("class", "btn btn-default btn-control btn-shuffle-false");
      }

      if(data.moreMusics === true && $("#load-more-musics").hasClass('disabled')) {
        $("#load-more-musics").removeClass('disabled');
      }

      $('.library-list-music').remove();
      $('#list-library').prepend(data.templateLibrary);

      if(data.currentMusic) {
        if(typeof(action) !== 'undefined' && action === "play") {
          if(!$("#btn-next, #dead-link").prop('disabled')) {
            freezeButtons();
          }
          else {
            $("#btn-next, #dead-link").prop('disabled', false);
          }
        }
        timeline(data.currentTimeLeft, data.currentTimePastPercent);
      }
      else {
        disabledBtn();
      }
      updatePlaylistCurrent(data);
    },
    error: logErrors
  });
}

// receive a message though the websocket from the server
function receiveMessage(message) {
  message = JSON.parse(message);
  if(message.update === true) {
    if(typeof(message.action) !== "undefined" && message.action === "play") {
      updateRemote(message.action);
    }
    else {
      updateRemote();
    }
  }
}


$(document).on('click', '.ordering-to-top, .ordering-move-up, .ordering-move-down, .ordering-to-bot', function() {
  var dataSend = {
    'music_id': $(this).closest("tr").attr("id"),
    'action': $(this).data("action"),
  };
  $.ajax({
    type: "POST",
    url: "/change-ordering/",
    data: dataSend,
    dataType: "json",
    success: function(data) {
      console.log("ok! " + data);
    },
    error: logErrors
  });
});
