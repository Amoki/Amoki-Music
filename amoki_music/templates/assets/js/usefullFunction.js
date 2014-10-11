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
});