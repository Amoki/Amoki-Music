$( document ).ready(function() {
	var hauteur = $(window).height() - 115;
	$(".LIB").height(hauteur);
//	$(".player").height(hauteur - 50);
	$(".list-lib").height(hauteur - 100);
//	$(".panel-playlist").height(hauteur - 300);     
	$( window ).resize(function() {
		if ($(window).width() > 992) {
			if ($(window).height() > 500) {
				var hauteur = $(window).height() - 110;
				$(".LIB").height(hauteur);
				//$(".player").height(hauteur - 50);
				$(".list-lib").height(hauteur - 100);
				//$(".panel-playlist").height(hauteur - 300); 
			}
		}
	});
});