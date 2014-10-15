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

	$(document).on ('submit', '.ajax', function (){
		var urlSubmit = $(this).attr('action');
		var dataSend = 'url=' + $(this).children('.video-id').val();
		var form =  $(this);
		if (urlSubmit == '/search-music/') {
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
						$.each(data.music, function(key, value){
							$(".list-group").append('<li class="list-group-item item-lib list-music" style="display:none;"><form action="/add-music/" method="post" class="pull-right ajax"><input class="video-id" type="hidden" value="'+ value.fields.video_id +'" name="url"><button class="btn btn-default btn-lg" type="submit" alt="Ajouter à la playlist" title="Ajouter à la playlist"><span class="glyphicon glyphicon-headphones"></span></button></form>'+ value.fields.name +'</li>');
						});
						if(data.regExp === true){
							maj_playlist_current(data, urlSubmit);
							alert(data.time_left+ ' et le pourcent : '+ data.time_past_percent);
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
				} else if (urlSubmit == '/shuffle/') {
					reset_timeline();
					if (data.shuffle === true){
						form.children("button").attr("value", "false");
						form.children("button").attr("class", "btn btn-default btn-control btn-shuffle-true");
						maj_playlist_current(data, urlSubmit);
					} else {
						form.children("button").attr("value", "true");
						form.children("button").attr("class", "btn btn-default btn-control btn-shuffle-false");
						maj_playlist_current(data, urlSubmit);
					}
				} else if (urlSubmit == '/next-music/') {
					reset_timeline();
					if(data.current){
						maj_playlist_current(data, urlSubmit);
					} else {
						disabled_btn();
					}
				} else if (urlSubmit == '/lien-mort/'){
					reset_timeline();
					if(data.current){
						maj_playlist_current(data, urlSubmit);
					} else {
						disabled_btn();
					}
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
		$("#lien-mort").attr('disabled', 'disabled');
	}
	function maj_playlist_current(data, url){
		$("#btn-next").removeAttr('disabled');
		$("#lien-mort").removeAttr('disabled');
		$('.playlist-ajax').children().remove();
		if(data.playlist.length > 0){
			$.each(data.playlist, function(key, value){
				$(".playlist-ajax").append('<tr class="playlist-item" id="'+ value.fields.video_id +'"><td>'+ value.fields.name +'</td><td><span class="badge">00:00</span></td></tr>');
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
	function reset_timeline(){
		clearInterval(intervalCompteur);
		$('.popover-on-top').css('width', '0%');
	}
});