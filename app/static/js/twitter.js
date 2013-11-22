// JS Fiddle
$('body').on('mouseenter','#social-hover',function(){
    $('#social-hover').animate({
        right: '150px'
    },250);
    $('#social-main').animate({
        right: '0px'
    },250);
});



$('body').on('mouseleave','#container',function(){
    $('#social-hover').animate({
        right: '0px'
    },250);
    $('#social-main').animate({
        right: '-150px'
    },250);
});


/*function grabtweet() {
	var url = "http://search.twitter.com/search.json?q=procrastinating, essay&callback=?";
	$.getJSON(url, handleRequest);
}
	
function handleRequest(data) {
	for (var i = 0; i < data.results.length; i++) {
		$('#twitter').append(buildTweet(data.results[i]))	
	}
	console.log(data);
}	

function buildTweet(tweet) {
	return "<div class='tweet'>" + tweet['text'] + "<p><strong><span class='xtra'>" + TwitterDateConverter(tweet['created_at']) + "</span></strong><span>"+ tweet['from_user'] + "</span></p></div>";
}

function TwitterDateConverter(time){
	var date = new Date(time),
		diff = (((new Date()).getTime() - date.getTime()) / 1000),
		day_diff = Math.floor(diff / 86400);
 
	if ( isNaN(day_diff) || day_diff < 0 || day_diff >= 31 )
		return;
 
	return day_diff == 0 && (
			diff < 60 && "just now" ||
			diff < 120 && "1 minute ago" ||
			diff < 3600 && Math.floor( diff / 60 ) + " minutes ago" ||
			diff < 7200 && "1 hour ago" ||
			diff < 86400 && Math.floor( diff / 3600 ) + " hours ago") ||
		day_diff == 1 && "Yesterday" ||
		day_diff < 7 && day_diff + " days ago" ||
		day_diff < 31 && Math.ceil( day_diff / 7 ) + " weeks ago";
}*/



