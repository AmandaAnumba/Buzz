function wikisearch(term) {
	//var query = $('#input').val();
	var query = term;
	var api = "http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=thumbnail&pilimit=1&titles="+query+"&callback=?";
	$.getJSON(api, handleRequest);
}

function handleRequest(url) {
	$('#wikipedia').empty();
	for (var pageId in url.query.pages) {
		if (url.query.pages.hasOwnProperty(pageId)) {
			if (url.query.pages[pageId].thumbnail) {
				console.log(url.query.pages[pageId].thumbnail.source);
				var output = url.query.pages[pageId].thumbnail.source;
			}
		}
	}
	var kw_img = buildImage(output);
	var doc_obj = document.getElementById("wikipedia");
	console.log(doc_obj);
	doc_obj.innerHTML += (kw_img);
}

function buildImage(photo) {
	var photo_html = "<div class='images'>";
	photo_html += "<img src='" + photo + "'/>";
	photo_html += "</div>";
	return photo_html;
}

