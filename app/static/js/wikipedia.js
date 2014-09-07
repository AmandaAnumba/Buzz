function imageSearch(term, genre, tw) {
	//Build up the URL for the request
	// var maxresults = 20;
	// var query = new String(term);
	var key = "boX7CdYBW+zsr99xjmIB9Dt4W7vhViJu65816FiBPjg";
	// var l = term.length;
	var uri = encodeURI(term).replace(/%20/g, "+");
	// console.log(uri);
	var url = "https://api.datamarket.azure.com/Bing/Search/Image?";
	var requestStr = url+"Query=%27"+uri+"%27&$format=json&Adult=%27Moderate%27&ImageFilters='Size:Medium'";
	//Return the promise from making an XMLHttpRequest to the server

	$.ajax({ 
		method:'GET',
		url: requestStr, 
		username: "",
		password:key,
		headers: {
        	"Authorization": "Basic " + base64_encode(":" + key)
    	},
		success: function(data, status) {
			var img = "<div class='artist_info' style='background: url("+data.d.results[0].MediaUrl+") no-repeat; background-size: cover; width:50px; height:50px; float:left;' data-toggle='popover' data-html='true' data-placement='right' data-trigger='hover' title='"+term+"' data-content='<small><strong>Trending songs: </strong>"+tw.song+"</small>'></div>";
			$('#for_'+genre).append(img);
    	}
	});
	

}


function base64_encode(data) {
  // http://kevin.vanzonneveld.net
  // +   original by: Tyler Akins (http://rumkin.com)
  // +   improved by: Bayron Guevara
  // +   improved by: Thunder.m
  // +   improved by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
  // +   bugfixed by: Pellentesque Malesuada
  // +   improved by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
  // +   improved by: Rafal Kukawski (http://kukawski.pl)
  // *     example 1: base64_encode('Kevin van Zonneveld');
  // *     returns 1: 'S2V2aW4gdmFuIFpvbm5ldmVsZA=='
  // mozilla has this native
  // - but breaks in 2.0.0.12!
  //if (typeof this.window['btoa'] == 'function') {
  //    return btoa(data);
  //}
  var b64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
  var o1, o2, o3, h1, h2, h3, h4, bits, i = 0,
    ac = 0,
    enc = "",
    tmp_arr = [];

  if (!data) {
    return data;
  }

  do { // pack three octets into four hexets
    o1 = data.charCodeAt(i++);
    o2 = data.charCodeAt(i++);
    o3 = data.charCodeAt(i++);

    bits = o1 << 16 | o2 << 8 | o3;

    h1 = bits >> 18 & 0x3f;
    h2 = bits >> 12 & 0x3f;
    h3 = bits >> 6 & 0x3f;
    h4 = bits & 0x3f;

    // use hexets to index into b64, and append result to encoded string
    tmp_arr[ac++] = b64.charAt(h1) + b64.charAt(h2) + b64.charAt(h3) + b64.charAt(h4);
  } while (i < data.length);

  enc = tmp_arr.join('');

  var r = data.length % 3;

  return (r ? enc.slice(0, r - 3) : enc) + '==='.slice(r || 3);

}
// function wikisearch(term) {
// 	//var query = $('#input').val();
// 	console.log(term);
// 	var api = "http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=thumbnail&pilimit=1&titles="+term+"&callback=?";
// 	$.getJSON(api, handleRequest);
// }

// function handleRequest(url) {
// 	console.log(url);
	

// 	// for (var pageId in url.query.pages) {
// 	// 	if (url.query.pages.hasOwnProperty(pageId)) {
// 	// 		if (url.query.pages[pageId].thumbnail) {
// 	// 			// console.log(url.query.pages[pageId].thumbnail.source);
// 	// 			var output = url.query.pages[pageId].thumbnail.source;
// 	// 		}
// 	// 	}
// 	// }


// 	// // var photo_html = "<img src='" + output + "'/>";
// 	// return output;
// }

