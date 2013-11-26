$(function() {
	// get the query from the clicked text
    $('#test p').click(function() {
        var query = ($(this).text());
		newsSearch(query);
		videoSearch(query);
		//imageSearch(query);
    });
});



// Bing News Search
// displays the title, source, and url of a news link 
// related to the query; sorted by date and relevance
//*************************************************************
//*************************************************************
//*************************************************************
var key = "boX7CdYBW+zsr99xjmIB9Dt4W7vhViJu65816FiBPjg";

function newsSearch(q) {
	//Build up the URL for the request
	var maxresults = 10;
	var query = new String(q);
	var l = query.length;
	var uri = encodeURI(query.slice(1, (l-1))).replace("%20", "+");
	var url = "https://api.datamarket.azure.com/Bing/Search/News?";
	var requestStr = url+"Query=%27"+uri+"%27&$top="+maxresults+"&$format=json&Adult=%27Moderate%27&NewsSortBy=%27Date%27";
	
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
			$('#news').empty();
			for (var i in data.d.results) {
				var title = data.d.results[i].Title;
				var source = data.d.results[i].Source;
				var link = data.d.results[i].Url;
				var snip = data.d.results[i].Description;
//				console.log(title);
//				console.log(source);
//				console.log(link);
				var output = "<div class='result'><span><a href="+link+" target='_blank'><p class='newsTitle'>"+ title +"<img src='static/Images/nw.png' /></p></a></span><p class='newsSource'>"+ source +"</p><p class='newsSnippet'>"+ snip +"</p></div>";
				document.getElementById('news').innerHTML += output;
			}
    	}
	})
}

// Bing Image Search
// displays the title, source, and url of a news link 
// related to the query; sorted by date and relevance
//*************************************************************
//*************************************************************
//*************************************************************
function imageSearch(q3) {
	//Build up the URL for the request
	var maxresults = 20;
	var query = new String(q3);
	var l = query.length;
	var uri = encodeURI(query.slice(1, (l-1))).replace("%20", "+");
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
			$('#images').empty();
			for (var i=0; i<maxresults; i++) {
				var imgUrl = data.d.results[i].MediaUrl;
				//console.log(imgUrl);
				var output = "<div class='imgresult'><img src='"+ imgUrl +"'/></div>";
				document.getElementById('images').innerHTML += output;
			}
    	}
	})
}



// Youtube Video Search
// returns relevant video search results based on query 
//*************************************************************
//*************************************************************
//*************************************************************
function videoSearch(q2) {
	//gather all parameters to make call to API
	var key = "AIzaSyBZXPwKLhBd64fIiewauHAN2B41MTdh5F0";
	var query = q2;
	var url = "https://www.googleapis.com/youtube/v3/search?";
	var results = 10;
	var api = url+"part=snippet&maxResults="+results+"&order=relevance&q="+query+"&type=video&key="+key+"&callback=?";
	$.getJSON(api, handleRequest2);
}

function handleRequest2(request) {
	//parse the json output to retrieve video results, title and channel
	$('#videos').empty();
	for (var i in request.items){
		var id = request.items[i].id.videoId;
		var title = request.items[i].snippet.title.toString();
		var ct = request.items[i].snippet.channelTitle;
		var output = "<div class='result'><p class='vidTitle'>"+ title +"</p><p class='vidDesc'>"+ ct +"</p>"+ build(id) +"</div>";
		document.getElementById('videos').innerHTML += output;
	}
}

function build(videoId) {
	var url = "<iframe id='ytplayer' type='text/html' width='275px' height='180px'";
	url += "src='http://www.youtube.com/embed/"+videoId+"?showinfo=0&controls=0' frameborder='0'/>";
	return url;
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