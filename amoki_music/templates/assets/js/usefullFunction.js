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

    $('span[data-time]').each(function(){
       $(this).html(updateTimePlaylistTemporaryFunction($(this).data("time")));
	});


	$(".btn").click(function(){
	    $(this).blur();
	});
	$(".popover-on-top").popover({
		placement : 'top',
		trigger : 'hover',
		content : '00:00'
	});
});

function maj_header_player(data){
	$(document).attr('title', data.music[0].fields.name);
	$(".header-player").children().remove();
	$(".player").children('.header-player')
	.append(
		$('<img/>', {
			id:'thumbnail',
			src: data.music[0].fields.thumbnail,
			width:'120px',
			height:'90px',
			class:'col-md-offset-1 col-md-3 img-responsive'
		}),
		$('<div/>', {
			class:'col-md-7 title_playing'
		})
		.append(
			$('<div/>', {
				class:'marquee'
			})
			.append(
				$('<a/>', {
					href:data.music[0].fields.url,
					class:'now-playing',
					text:data.music[0].fields.name
				})
			)
		)
	);
	$('#url-next').val(data.music[0].fields.url);
	$('#url-dead-link').val(data.music[0].fields.url);
}
function disabled_btn(){
	$(document).attr('title', 'Amoki\'s musics');
	$(".header-player").children().remove();
	$('.header-player').append('<div class="col-md-12 title"><div class="marquee"><span class="now-playing">No music :\'( Add yours now !</span></div></div>');
	$("#btn-next").attr('disabled', 'disabled');
	$("#dead-link").attr('disabled', 'disabled');
	$(".progress-bar").stop();
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
			$(".playlist-ajax")
			.append(
				$('<tr/>', {
					id:value.fields.url,
					class:'playlist-item'
				})
				.append(
					$('<td/>', {
						text:value.fields.name
					}),
					$('<td/>')
					.append(
						$('<span/>', {
							class:'badge',
							text: updatePopover(value.fields.duration)
						})
					)
				)
			);
		});
	} else if (data.shuffle) {
		$(".playlist-ajax").append('<tr class="empty"><td>Shuffle activated...<br /><br />Let the music be your guide</span></td></tr>');
	} else {
		$(".playlist-ajax").append('<tr class="empty"><td>No more musics in the playlist !</td></tr>');
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