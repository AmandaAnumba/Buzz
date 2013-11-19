function display() {
	var city = $('#cities :checkbox:checked');
	var selected = city.length;
	
	if (selected == 2) {
		var title = new Array();
		
		for (var i = 0; i < selected; i++) {
			title[i] = city[i].name;
			console.log(title[i]);	
			$('label#c1').empty();
			$('label#c2').empty();
			
		}
		$('label#c1').append(title[0]);
		$('label#c2').append(title[1]);
		
	}
	
	
}