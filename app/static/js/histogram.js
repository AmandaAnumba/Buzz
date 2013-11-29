// for the histogram that displays on the discover page

$("info").mouseover(function () {
	var city = document.getElementById("city");

	$.getJSON( "static/json/"+city+"_media_values.json", function( data ) {

		var container = document.getElementById("histchart");

		$.each( data, function( i, top_keywords ) {
		  	var list = document.createElement("ul");
		    list.className = "terms";
		    container.appendChild(list);

		    for (i==0; i<5; i++) {
		    	var list-inner = document.createElement("li");
				list.appendChild(list-inner);
				
				var span = document.createElement("span");
				span.className = "pre";
				list-inner.appendChild(span);

				// calculate the count here
				// count = 
				// it effects the width of the histogram
				span.innerHTML = "<div class='count'>"+count+"</div>";

				var bar-wrap = document.createElement("div");
				bar-wrap.className = "inner";
				list-inner.appendChild(bar-wrap);

				var bar = document.createElement("div");
				bar.className = "bar";
				// width = 
				bar.setAttribute("width", width);
				// calculate the width here, in percents 
				// ex: count for top trending topic divided by count 
				// for second top trending top * 100
				bar.innerHTML = '<p class="text2">' + keyword.label + '</p>';
				inner.appendChild(bar);

		  	}		
		});
	}); 
});
