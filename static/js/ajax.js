$(document).on ('submit', '.ajax-shuffle', function (e){
	e.preventDefault();
	var form =  $(this);
	var urlSubmit = form.attr('action');
	var dataSend = 'shuffle=' + encodeURIComponent(form.children("button").val());
	
	$.ajax({
		type: "POST",
		url: urlSubmit,
		data: dataSend,
		dataType: "json",
		success: function(data) {
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
		},
		error : function(resultat, statut, erreur){
				console.log(resultat.responseText);
				console.log(statut);
				console.log(erreur);
      	},
	});
});

$(document).on ('submit', '.ajax-next, .ajax-dead-link', function (e){
	e.preventDefault();
	var form =  $(this);
	var urlSubmit = form.attr('action');
	var dataSend = 'url=' + encodeURIComponent(form.children('.url').val());
	
	$.ajax({
		type: "POST",
		url: urlSubmit,
		data: dataSend,
		dataType: "json",
		success: function(data) {
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
		},
		error : function(resultat, statut, erreur){
				console.log(resultat.responseText);
				console.log(statut);
				console.log(erreur);
	  	},
	});
});

$(document).on ('submit', '.ajax-search', function (e){
	e.preventDefault();
	var form =  $(this);

	if (form.children('.url').val().trim() === '' || form.children('.url').val().trim() === null){
		$(".youtube-list-music").slideUp();
		$(".youtube-list-music").promise().done(function(){
			$(".youtube-list-music").remove();
			$("#list-youtube").append('<li class="list-group-item item-lib youtube-list-music"><div class="row"><p class="col-xs-10">Enter your search in the field above</p><i class="fa fa-level-up fa-2x col-xs-2"></i></div></li>');
			$(".youtube-list-music").slideDown();
		});
		return;
	}

	form.children("span").children("button").children("i").attr("class", "fa fa-refresh fa-spin");
	form.children("span").children("button").attr('disabled', 'disabled');
	var urlSubmit = form.attr('action');
	var dataSend = 'url=' + encodeURIComponent(form.children('.url').val());
	
	$.ajax({
		type: "POST",
		url: urlSubmit,
		data: dataSend,
		dataType: "json",
		success: function(data) {
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
									class:'ajax-add-music col-xs-2',
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
		},
		error : function(resultat, statut, erreur){
				console.log(resultat.responseText);
				console.log(statut);
				console.log(erreur);
	  	},
	});
});

$(document).on ('submit', '.ajax-add-music', function (e){
	e.preventDefault();
	var form =  $(this);
	var urlSubmit = form.attr('action');
	var dataSend = {'url':encodeURIComponent($(this).children('.url').val()), 'requestId':encodeURIComponent($(this).children('.requestid').val())};

	form.children("button").children("span").attr("class", "fa fa-refresh fa-spin");
	form.children("button").attr('disabled', 'disabled');

	$.ajax({
		type: "POST",
		url: urlSubmit,
		data: dataSend,
		dataType: "json",
		success: function(data) {
			maj_playlist_current(data, urlSubmit);
			timeline(data.time_left, data.time_past_percent);
			form.children("button").children("span").attr('class', 'glyphicon glyphicon-headphones');
			form.children("button").removeAttr('disabled');
			modal_confirm($('#modal-add-music'));			
		},
		error : function(resultat, statut, erreur){
			console.log(resultat.responseText);
			console.log(statut);
			console.log(erreur);
	  	},
	});
});