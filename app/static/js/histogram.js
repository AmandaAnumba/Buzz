// for the histogram that displays on the discover page

$(function() {
	//$.getJSON( "static/json/"+city+"_media_values.json", function( data ) {
	var city = document.getElementById("city").innerHTML;
	var sampledata = {
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