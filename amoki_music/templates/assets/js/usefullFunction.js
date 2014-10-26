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
	var myCounter = new Countdown({
	    onCounterEnd: function(){} // final action
	});

	$(document).on ('submit', '.ajax', function (){
		var urlSubmit = $(this).attr('action');
		var form =  $(this);
		var dataSend = 'url=' + encodeURIComponent($(this).children('.url').val());
		if (urlSubmit == '/search-music/') {
			if ($(this).children('.url').val().trim() === '' || $(this).children('.url').val().trim() === null){
				$(".youtube-list-music").slideUp();
				$(".youtube-list-music").promise().done(function(){
					$(".youtube-list-music").remove();
					$("#list-youtube").append('<li class="list-group-item item-lib youtube-list-music"><div class="row"><p class="col-xs-10">Enter your search in the field above</p><i class="fa fa-level-up fa-2x col-xs-2"></i></div></li>');
					$(".youtube-list-music").slideDown();
				});
				return false;
			}
			form.children("span").children("button").children("i").attr("class", "fa fa-refresh fa-spin");
			form.children("span").children("button").attr('disabled', 'disabled');
		} else if (urlSubmit == '/add-music/') {
			form.children("button").children("span").attr("class", "fa fa-refresh fa-spin");
			form.children("button").attr('disabled', 'disabled');
			dataSend = {'url':encodeURIComponent($(this).children('.url').val()), 'requestId':encodeURIComponent($(this).children('.requestid').val())};
		} else if (urlSubmit == '/shuffle/') {
			dataSend = 'shuffle=' + encodeURIComponent($(this).children("button").val());
		}
		$.ajax({
			type: "POST",
			url: urlSubmit,
			data: dataSend,
			dataType: "json",
			success: function(data) {
				if (urlSubmit == '/search-music/') {
					$(".youtube-list-music").slideUp();
					$(".youtube-list-music").promise().done(function(){
						$(".youtube-list-music").remove();
						var i=0;
						if(data.music.length > 0){
							$.each(data.music, function(key, value){
								$('#list-youtube')
								.append(
									$('<li/>', {
										id:'li-'+i,
										class: 'list-group-item item-lib youtube-list-music row row-list-item',
										style: 'display:none',
										'data-toggle':'popover',
										'data-placement':'left',
										'data-content': '<p>'+value.fields.description+'</p>'

									})
									.append(
										$('<img/>', {
											class:'col-xs-3',
											src:value.fields.thumbnail,
											style:'padding:0px'
										}),
										$('<div/>', {
											class: 'col-xs-7',
											style:'padding-right:0px'
										})
										.append(
											$('<div/>', {
												class:'row',
											})
											.append(
												$('<div/>', {
													class:'col-xs-12',
													style:'min-height:45px',
													text: value.fields.name,
												})
											),
											$('<div/>', {
												class:'row'
											})
											.append(
												$('<div/>', {
													class:'col-xs-8',
													style:'color:black;font-weight:normal;',
													text:value.fields.views+ ' views'
												}),
												$('<div/>', {
													class:'col-xs-4'
												})
												.append(
													$('<span/>', {
														class:'badge',
														text:updateTimePlaylistTemporaryFunction(value.fields.duration)
													})
												)
											)
										),
										$('<form/>', {
											class:'ajax col-xs-2',
											action:'/add-music/',
											method:'post'
										})
										.append(
											$('<input/>', {
												class:'url',
												type:'hidden',
												value: value.fields.url,
												name:'url'
											}),
											$('<input/>', {
												class:'requestid',
												type:'hidden',
												value: value.fields.requestId,
												name:'requestId'
											}),
											$('<button/>', {
												class:'btn btn-default btn-lg',
												type:'submit',
												alt:'Ajouter à la playlist',
												title:'Ajouter à la playlist'
											})
											.append(
												$('<span/>',{
													class:'glyphicon glyphicon-headphones'
												})
											)
										),
										$('<div/>', {
											class:'row'
										})
									)
								);
								$('#li-'+i).popover({
									html:'true',
									container: 'body',
								    trigger: 'hover'
								});
								i++;
							});
						} else {
							$('#list-youtube')
							.append(
								$('<li/>', {
									id:'li-'+i,
									class: 'list-group-item item-lib youtube-list-music row row-list-item',
									style: 'display:none'
								})
								.append(
									$('<p/>', {
										text:'No result'
									})
								)
							);
						}
						if(data.regExp === true){
							maj_playlist_current(data, urlSubmit);
							timeline(data.time_left, data.time_past_percent);
						}
						$(".youtube-list-music").slideDown();
						$(".youtube-list-music").promise().done(function(){
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
						timeline(data.time_left, data.time_past_percent);
						modal_confirm($('#modal-shuffle-on'));
					} else {
						form.children("button").attr("value", "true");
						form.children("button").attr("class", "btn btn-default btn-control btn-shuffle-false");
						maj_playlist_current(data, urlSubmit);
						modal_confirm($('#modal-shuffle-off'));
					}
				} else if (urlSubmit == '/next-music/' || urlSubmit == '/dead-link/') {
					if(data.current){
						maj_playlist_current(data, urlSubmit);
						timeline(data.time_left, data.time_past_percent);
					} else {
						disabled_btn();
					}
					if(data.skipped){
						modal_confirm($('#modal-next-music'));
					} else {
						modal_confirm($('#modal-next-error'));
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
	/*
	$(function() {
		$('.library-list-music').endlessScroll({
			fireOnce: true,
			insertAfter: ".library-list-music:last",
			content: function() {
				return '<li>' + i + '</li>';
			}
		});
	});
	*/
});
