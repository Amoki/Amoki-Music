var csrftoken = $.cookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

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
				modal_confirm($('#modal-shuffle-on'));
			} else {
				form.children("button").attr("value", "true");
				form.children("button").attr("class", "btn btn-default btn-control btn-shuffle-false");
				modal_confirm($('#modal-shuffle-off'));
			}
			timeline(data.time_left, data.time_past_percent);
			maj_playlist_current(data, urlSubmit);
			updateDataTime();
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
			if(data.current_music){
				maj_playlist_current(data, urlSubmit);
				updateDataTime();
				timeline(data.time_left, data.time_past_percent);
			} else {
				disabled_btn();
			}
			modal_confirm($('#modal-next-music'));
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
		$("#list-youtube").slideUp();
		$("#list-youtube").promise().done(function(){
			$(".youtube-list-music").remove();
			$("#list-youtube").append('<li class="list-group-item item-lib youtube-list-music"><div class="row"><p class="col-xs-10">Enter your search in the field above</p><i class="fa fa-level-up fa-2x col-xs-2"></i></div></li>');
			$("#list-youtube").slideDown();
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
			if(data.current_music){
					maj_playlist_current(data);
					timeline(data.time_left, data.time_past_percent);
					$("#btn-search").children("i").attr("class", "fa fa-youtube-play");
					$("#btn-search").removeAttr('disabled');
					modal_confirm($('#modal-add-music'));
					updateDataTime();
			} else {
				$("#tab_btn_youtube").addClass("active");
				$("#youtube").addClass("active");
				$("#tab_btn_library").removeClass("active");
				$("#library").removeClass("active");
				$("#list-youtube").slideUp();
				$("#list-youtube").promise().done(function(){
					$(".youtube-list-music").remove();
					$("#list-youtube").html(data.template_library);
					updateDataTime();
					$("#list-youtube").slideDown();
					$("#list-youtube").promise().done(function(){
						$("#btn-search").children("i").attr("class", "fa fa-youtube-play");
						$("#btn-search").removeAttr('disabled');
					});
				});
			}
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
	var dataSend = {'url':encodeURIComponent($(this).children('.url').val()), 'requestId': encodeURIComponent($(this).children('.requestId').val())};
	form.children("button").children("span").attr("class", "fa fa-refresh fa-spin");
	form.children("button").attr('disabled', 'disabled');

	$.ajax({
		type: "POST",
		url: urlSubmit,
		data: dataSend,
		dataType: "json",
		success: function(data) {
			maj_playlist_current(data);
			updateDataTime();
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

$(document).on ('submit', '.ajax-volume', function(e){
	e.preventDefault();
	var form =  $(this);
	var urlSubmit = form.attr('action');
	var dataSend = 'volume_change='+encodeURIComponent(form.children(".volume_clicked").val());

	$.ajax({
		type: "POST",
		url: urlSubmit,
		data: dataSend,
		dataType: "json",
		success: function(data){
			form.children(".volume_clicked").removeClass("volume_clicked");
		},
		error : function(resultat, statut, erreur){
			console.log(resultat.responseText);
			console.log(statut);
			console.log(erreur);
	  	},
	});
});

$(document).on('submit', '.ajax_music_inifi_scroll', function(e){
	e.preventDefault();
	var form =  $(this);
	var urlSubmit = form.attr('action');
	var dataSend = 'page='+encodeURIComponent(form.children("#page").val());
	$("<li id='spinner_Library' class='list-group-item item-lib library-list-music row row-list-item' style='color:black'><i class='fa fa-spinner fa-4x fa-spin'></i></li>").insertBefore(form.closest('li'));

	$.ajax({
		type: "POST",
		url: urlSubmit,
		data: dataSend,
		dataType: "json",
		success: function(data){
			$(data.template).insertBefore(form.closest('li'));
			form.children("#page").val(parseInt(form.children("#page").val()) + 1);
			updateDataTime();
			$("#spinner_Library").remove();
		},
		error : function(resultat, statut, erreur){
			console.log(resultat.responseText);
			console.log(statut);
			console.log(erreur);
	  	},
	});
});

function update_player(){
	$.ajax({
		type: "POST",
		url: "/update-player/",
		data: "",
		dataType: "json",
		success: function(data){
			if (data.shuffle === true){
				$("#btn-shuffle").attr("value", "false");
				$("#btn-shuffle").attr("class", "btn btn-default btn-control btn-shuffle-true");		
			} else {
				$("#btn-shuffle").attr("value", "true");
				$("#btn-shuffle").attr("class", "btn btn-default btn-control btn-shuffle-false");
			}

			if(data.current_music){
				timeline(data.time_left, data.time_past_percent);
				maj_playlist_current(data);
			} else {
				disabled_btn();
			}
			updateDataTime();
		},
		error : function(resultat, statut, erreur){
			console.log(resultat.responseText);
			console.log(statut);
			console.log(erreur);
	  	},
	});
}
