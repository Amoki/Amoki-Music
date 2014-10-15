function timeline(current_time_left, current_time_past_percent){
	var actual_time = parseInt(current_time_left);
	$('.progress-bar').css("width", current_time_past_percent+'%');
	$('.progress-bar').animate({
		width: "100%"},
		actual_time);

	var popover = $('.popover-on-top').data('bs.popover');
	var heures = Math.floor(actual_time / 3600);
	var minutes = Math.floor((actual_time - (heures * 3600)) / 60);
	var secondes = actual_time - (heures * 3600) - (minutes * 60) ;
	var printedTime = "";
	function compteur() {
		if(secondes === 0) {
			secondes = 59;
			if(minutes === 0) {
				minutes = 59;
				if(heures === 0){
					clearInterval(intervalCompteur);
					return true;
				}
				else
					heures--;
			}
			else
				minutes--;
		}
		else {
			secondes--;
		}
		var stantardize = function(num){
			if (num < 10) {
				printedTime += "0";
			}
		};
		printedTime = heures+":";
		stantardize(minutes);
		printedTime += minutes+":";
		stantardize(secondes);
		printedTime += secondes;
		$('.popover-on-top').attr('data-content', printedTime);
		popover.setContent();
		popover.$tip.addClass(popover.options.placement);
	}
	var intervalCompteur = setInterval(compteur,1000);
	return intervalCompteur;
}