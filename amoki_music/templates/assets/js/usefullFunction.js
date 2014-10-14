$( document ).ready(function() {
	var hauteur = $(window).height() - 115;
	$(".LIB").height(hauteur);
//	$(".player").height(hauteur - 50);
	$(".list-lib").height(hauteur - 100);
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
			$(".list-lib").height(hauteur - 100);
			//$(".panel-playlist").height(hauteur - 300); 
		}
	});

	$(".btn").click(function(){
	    $(this).blur();
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
		} else if (urlSubmit == '/next-music/'){
			dataSend = 'play_next='+$(this).children("button").val();
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
						$.each(data['music'], function(key, value){
							$(".list-group").append('<li class="list-group-item item-lib list-music" style="display:none;"><form action="/add-music/" method="post" class="pull-right ajax"><input class="video-id" type="hidden" value="'+ value.fields.video_id +'" name="url"><button class="btn btn-default btn-lg" type="submit" alt="Ajouter à la playlist" title="Ajouter à la playlist"><span class="glyphicon glyphicon-headphones"></span></button></form>'+ value.fields.name +'</li>');
						});
						if(data['regExp'] === true){
							maj_playlist(data, form);
						}
						$(".list-music").slideDown();
						$(".list-music").promise().done(function(){
							$("#btn-search").children("i").attr("class", "fa fa-youtube-play");
							$("#btn-search").removeAttr('disabled');
						});
					});
				} else if (urlSubmit == '/add-music/') {
					maj_playlist(data, form);
				} else if (urlSubmit == '/shuffle/') {
					if (data['shuffle'] === true){
						form.children("button").attr("value", "false");
						form.children("button").attr("class", "btn btn-default btn-control btn-shuffle-true");
						$("#btn-next").removeAttr('disabled');
						if($(".title_playing").length < 1) {
							maj_header_player(data);
						}
					} else {
						form.children("button").attr("value", "true");
						form.children("button").attr("class", "btn btn-default btn-control btn-shuffle-false");
					}
				} else if (urlSubmit == '/next-music/') {
					if(data['current']){
						if(data['playlist'].length > 0){
							maj_header_player(data);
							$(".playlist-ajax").children("tr:first").remove();
						}
					} else {
						$(document).attr('title', 'Amoki\'s musics');
						$(".header-player").children().remove();
						$('.header-player').append('<div class="col-md-12 title"><div class="marquee"><span class="now-playing">No music :\'( Add yours now !</span></div></div>');
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
	function maj_playlist(data, form){
		if($(".title_playing").length) {
			$(".empty").remove();
			$.each($(".playlist-item"), function(){
				if(this.id == data['music'][0].fields.video_id){
					this.remove();
				}
			});
			$(".playlist-ajax").append('<tr class="playlist-item" id="'+ data['music'][0].fields.video_id +'"><td>'+ data['music'][0].fields.name +'</td><td><span class="badge">00:00</span></td></tr>');
		} else {
			maj_header_player(data);
		}
		$("#btn-next").removeAttr('disabled');
		form.children("button").children("span").attr('class', 'glyphicon glyphicon-headphones');
		form.children("button").removeAttr('disabled');
	}
	function maj_header_player(data){
		$(document).attr('title', data['music'][0].fields.name);
		$(".header-player").children().remove();
		$(".player").children('.header-player').append('<img id="thumbnail" src="'+ data['music'][0].fields.thumbnail +'" width="120px" height="90px" class="col-md-offset-1 col-md-3 img-responsive"></img><div class="col-md-7 title_playing"><div class="marquee"><a href="https://www.youtube.com/watch?v='+ data['music'][0].fields.video_id +'" class="now-playing">'+ data['music'][0].fields.name +'</a></div></div>');
	}
});