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
/*
	//Override de la fonction "contains" pour permettre une recherche case-insensitive
	jQuery.expr[':'].contains = jQuery.expr.createPseudo(function(arg) {
		return function( elem ) {
			return jQuery(elem).text().toUpperCase().indexOf(arg.toUpperCase()) >= 0;
		};
	});
	//Recherche basée sur le champs input "input-search"
	$("#input-search").keyup(function(){
		var strToSearch = $("#input-search").val();
		if (strToSearch.length > 2 ){
			$(".list-music:not(:contains('"+strToSearch+"'))").slideUp();
			$(".list-music:contains('"+strToSearch+"')").slideDown();
		} else if (strToSearch.length === 0){
			$(".list-music").slideDown();
		}
	});


	$("#ajax").submit( function() {
		var urlSubmit = $(this).attr('action');
		$.ajax({  
			type: "POST",
			url: urlSubmit,
			dataType: "json",
			success: function(data) {
				$('.list-music').slideUp('fast', function(){
					$.each(data, function(key, value){

					});
				});
			}
		});
		return false;
	});
*/
});