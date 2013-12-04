// for the histogram that displays on the discover page

$(function() {

	citieslist.forEach(function(city) {

		$.getJSON( "static/json/" + city + "_media_values.json", function( data ) {

			$('#terms' + city).append("<li><div class='inner'><span class='pre'>");
			
			$.each( data, function( i, keyword ) {
				//console.log(keyword)
		        if ( i === 5 ) {
			        $('#terms' + city.replace(/ /g,"_")).append("</div></li>");
			        
			        //console.log($('#terms' + city.replace(/ /g,"_")))
			       // $("<br/>").insertAfter('.bar' + city);
			        return false;
		    	}
		    	
		    	else {
		    		valadd = keyword.value * 20;
		    		val = 20 + valadd;
		    		key = keyword.label;
		    		$('#terms' + city.replace(/ /g,"_")).append("<span class='pre'><div class='count'>"+(i + 1)+"</div></span><div class='bar'" + city.replace(/ /g,"_") + " style='width:"+val+"%'><p class='text2'>" + key + "</p></div><br/><br/>");
		    	}
		    });
			
			$("<br/>").insertAfter('.bar' + city.replace(/ /g,"_"));
		});
	});
});
	/*var sampledata = {
		"Rihanna": "85",
		"Macklemore": "75",
		"One Direction": "58",
		"Skrillex": "36",
		"Avicii": "29"
	};

	$.each(sampledata, function(key, val) {
		$('.terms').append("<li><div class='inner'><span class='pre'><div class='count'>"+val+"</div></span><div class='bar' style='width:"+val+"%'><p class='text2'>" + key + "</p></div></div></li>");
	}); 

	$("<br/>").insertAfter('.bar');
});
});*/