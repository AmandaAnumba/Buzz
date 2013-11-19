function wikisearch() {
	var query = $('#input').val();
	var api = "http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=thumbnail&pilimit=1&titles="+query+"&callback=?";
	$.getJSON(api, handleRequest);
}

function handleRequest(url) {
	$('#wikipedia').empty();
	for (var pageId in url.query.pages) {
		if (url.query.pages.hasOwnProperty(pageId)) {
			console.log(url.query.pages[pageId].thumbnail.source);
			var output = url.query.pages[pageId].thumbnail.source;
		}
	}
	$('#wikipedia').append(buildImage(output));
}

function buildImage(photo) {
	var photo_html = "<div class='images'>";
	photo_html += "<img src='" + photo + "'/>";
	photo_html += "</div>";
	return photo_html;
}

