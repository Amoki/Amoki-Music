$( document ).ready(function() {
	var hauteur = $(window).height() - 115;
	if ($(window).height() > 765) {
		hauteur = $(window).height() - 115;
	} else {
		hauteur = 650;
	}
	$(".LIB").height(hauteur);
//	$(".player").height(hauteur - 50);
	$(".list-lib").height(hauteur - 90);
	$(".tab-content").height(hauteur - 130);
//	$(".panel-playlist").height(hauteur - 300);     
	$( window ).resize(function() {
		if ($(window).width() > 992) {
			if ($(window).height() > 765) {
				hauteur = $(window).height() - 115;
			} else {
				hauteur = 650;
			}
			$(".LIB").height(hauteur);
			//$(".player").height(hauteur - 50);
			$(".list-lib").height(hauteur - 90);
			$(".tab-content").height(hauteur - 130);
			//$(".panel-playlist").height(hauteur - 300); 
		}
	});

	$(".btn").click(function(){
	    $(this).blur();
	});
	$(".popover-on-top").popover({
		placement : 'top',
		trigger : 'hover',
		content : '0:00:00'
	});
	var myCounter = new Countdown({  
	    onCounterEnd: function(){} // final action
	});

	$(document).on ('submit', '.ajax', function (){
		var urlSubmit = $(this).attr('action');
		var form =  $(this);
		var dataSend = 'url=' + $(this).children('.video-id').val();
		if (urlSubmit == '/search-music/') {
			if ($(this).children('.video-id').val().trim() === '' || $(this).children('.video-id').val().trim() === null){
				$(".list-music").slideUp();
				$(".list-music").promise().done(function(){
					$(".list-music").remove();
					$(".list-group").append('<li class="list-group-item item-lib list-music"><div class="row"><p class="col-xs-10">Enter your search in the field above</p><i class="fa fa-level-up fa-2x col-xs-2"></i></div></li>');
					$(".list-music").slideDown();
				});
				return false;
			}
			form.children("span").children("button").children("i").attr("class", "fa fa-refresh fa-spin");
			form.children("span").children("button").attr('disabled', 'disabled');
		} else if (urlSubmit == '/add-music/') {
			form.children("button").children("span").attr("class", "fa fa-refresh fa-spin");
			form.children("button").attr('disabled', 'disabled');
		} else if (urlSubmit == '/shuffle/') {
			dataSend = 'shuffle=' + $(this).children("button").val();
		}
		$.ajax({
			type: "POST",
			url: urlSubmit,
			data: dataSend,
			dataType: "json",
			success: function(data) {
				if (urlSubmit == '/search-music/') {
					$(".list-music").slideUp();
					$(".list-music").promise().done(function(){
						$(".list-music").remove();
						if(data.music.length > 0){
							$.each(data.music, function(key, value){
								$(".list-group").append('<li class="list-group-item item-lib list-music row row-list-item" style="display:none;"><div class="col-xs-10">'+ value.fields.name +'</div><form action="/add-music/" method="post" class="ajax col-xs-2"><input class="video-id" type="hidden" value="'+ value.fields.video_id +'" name="url"><button class="btn btn-default btn-lg" type="submit" alt="Ajouter à la playlist" title="Ajouter à la playlist"><span class="glyphicon glyphicon-headphones"></span></button></form></li>');
							});
						} else {
							$(".list-group").append('<li class="list-group-item item-lib list-music" style="display:none;"><p>No result</p></li>');
						}
						if(data.regExp === true){
							maj_playlist_current(data, urlSubmit);
							timeline(data.time_left, data.time_past_percent);
						}
						$(".list-music").slideDown();
						$(".list-music").promise().done(function(){
							$("#btn-search").children("i").attr("class", "fa fa-youtube-play");
							$("#btn-search").removeAttr('disabled');
						});
					});
				} else if (urlSubmit == '/add-music/') {
					maj_playlist_current(data, urlSubmit);
					timeline(data.time_left, data.time_past_percent);
					form.children("button").children("span").attr('class', 'glyphicon glyphicon-headphones');
					form.children("button").removeAttr('disabled');
					modal_confirm($('#modal-add-music'));
				} else if (urlSubmit == '/shuffle/') {
					if (data.shuffle === true){
						form.children("button").attr("value", "false");
						form.children("button").attr("class", "btn btn-default btn-control btn-shuffle-true");
						maj_playlist_current(data, urlSubmit);
						modal_confirm($('#modal-shuffle-on'));
					} else {
						form.children("button").attr("value", "true");
						form.children("button").attr("class", "btn btn-default btn-control btn-shuffle-false");
						maj_playlist_current(data, urlSubmit);
						modal_confirm($('#modal-shuffle-off'));
					}
				} else if (urlSubmit == '/next-music/') {
					if(data.current){
						maj_playlist_current(data, urlSubmit);
						timeline(data.time_left, data.time_past_percent);
					} else {
						disabled_btn();
					}
					modal_confirm($('#modal-next-music'));
				} else if (urlSubmit == '/dead-link/'){
					if(data.current){
						maj_playlist_current(data, urlSubmit);
						timeline(data.time_left, data.time_past_percent);
					} else {
						disabled_btn();
					}
					modal_confirm($('#modal-dead-link'));
				}
			},
			error : function(resultat, statut, erreur){
				console.log(resultat.responseText);
				console.log(statut);
				console.log(erreur);
      		},
		});
		return false;
	});
	function maj_header_player(data){
		$(document).attr('title', data.music[0].fields.name);
		$(".header-player").children().remove();
		$(".player").children('.header-player').append('<img id="thumbnail" src="'+ data.music[0].fields.thumbnail +'" width="120px" height="90px" class="col-md-offset-1 col-md-3 img-responsive"></img><div class="col-md-7 title_playing"><div class="marquee"><a href="https://www.youtube.com/watch?v='+ data.music[0].fields.video_id +'" class="now-playing">'+ data.music[0].fields.name +'</a></div></div>');
	}
	function disabled_btn(){
		$(document).attr('title', 'Amoki\'s musics');
		$(".header-player").children().remove();
		$('.header-player').append('<div class="col-md-12 title"><div class="marquee"><span class="now-playing">No music :\'( Add yours now !</span></div></div>');
		$("#btn-next").attr('disabled', 'disabled');
		$("#dead-link").attr('disabled', 'disabled');
		$(".progress-bar").css('width', '0%');
		myCounter.stop();
	}
	function maj_playlist_current(data, url){
		myCounter.stop();
		myCounter.start(data.time_left);
		$("#btn-next").removeAttr('disabled');
		$("#dead-link").removeAttr('disabled');
		$('.playlist-ajax').children().remove();
		if(data.playlist.length > 0){
			$.each(data.playlist, function(key, value){
				$(".playlist-ajax").append('<tr class="playlist-item" id="'+ value.fields.video_id +'"><td>'+ value.fields.name +'</td><td><span class="badge">'+ updatePopover(value.fields.duration) +'</span></td></tr>');
			});
		} else if (data.shuffle) {
			$(".playlist-ajax").append('<tr class="empty"><td><span style="font-size:22px;font-weight:bold;text-align:center;color:black;">Shuffle activated...<br /><br />Let the music be your guide</span></td></tr>');
		} else {
			$(".playlist-ajax").append('<tr class="empty"><td><span style="margin-left:-22px;font-size:22px;font-weight:bold;text-align:center; color: black;">No more musics in the playlist !</span></td></tr>');		
		}
		if (url !== '/add-music/' && url !== '/search-music/'){
			maj_header_player(data);
		} else if ($('.title').length){
			maj_header_player(data);
		}
	}
	function modal_confirm(target){
		target.modal({
			'show':true,
			'backdrop':false
		}).on('shown.bs.modal', function(){
			setTimeout(function(){target.modal('hide');}, 1000);
		});
	}
});