$(document).ready(function() {
	$('span.timestamp').html(function(index, oldhtml) {
		return formatTime(oldhtml);
	});
	$('a.button').click(function() {
		$('#ajax').slideDown('slow');
		$('a.button').slideUp('slow');
		$.getJSON($('#next').val() + '&callback=?', function(data) {
			$.each(data.data, function(i, item){
				if (item.message && item.message.length > 10) { $('#table').append(getFML(item)); }
			});
			$('#next').val(data.paging.next);
			$('#ajax').slideUp('slow');
			$('a.button').slideDown('slow');
		});
	});
});

function getFML(data) {
	return "<tr><td><a href='http://www.facebook.com/profile.php?id=" + data.from.id + "' target='_blank'><img src='http://graph.facebook.com/" 
	+ data.from.id + "/picture?type=square' /></a></td><td><div class='entry'>" + $('<span/>').text(data.message).html() 
	+ "<div class='status_info'><a href='http://www.facebook.com/profile.php?id=" + data.from.id + "' target='_blank'>" + data.from.name 
	+ "</a> <span class='timestamp'>" + formatTime(data.created_time) + "</span></div></div></td></tr><tr><td colspan=2><hr/></td></tr>";
}

function formatTime(time) {
	var d = new Date();
	d.setISO8601(time);
	return d.toRelativeString();
}

Date.prototype.getFormattedMinutes = function() {
	return this.getMinutes() < 10 ? '0' + this.getMinutes() : this.getMinutes();
}

Date.prototype.getFormattedTime = function() {
	if (this.getHours() > 12) { return (this.getHours() - 12) + ':' + this.getFormattedMinutes() + 'pm'; }
	return (this.getHours() == 0 ? 12 : this.getHours()) + ':' + this.getFormattedMinutes() + 'am';
}

Date.prototype.toRelativeString = function() {
	var curTime = new Date();
	var millis = curTime.getTime() - this.getTime();
	if (millis < 3600000) {
		//occured within the last hour
		var minutes = Math.floor(millis/60000);
		var seconds = Math.floor(millis/1000);
		if (minutes > 0) { return minutes == 1 ? '1 minute ago' : minutes + ' minutes ago'; }
		if (seconds > 0) { return seconds == 1 ? '1 second ago' : seconds + ' seconds ago'; }
	}
	var yesterday = new Date(curTime.getFullYear(), curTime.getMonth(), curTime.getDate()-1);
	//old status, use default date format
	if (millis > curTime - yesterday.getTime()) { return 'at ' + this.getFormattedTime() + ' on ' + this.toLocaleDateString(); }
	var today = new Date(curTime.getFullYear(), curTime.getMonth(), curTime.getDate());
	//yesterday time format
	if (millis > curTime.getTime() - today.getTime()) { return 'yesterday at ' + this.getFormattedTime(); }
	//today time format
	if (millis > 3600000) { return 'today at ' + this.getFormattedTime() }
	return 'just now';
}

//credit to http://delete.me.uk/2005/03/iso8601.html
Date.prototype.setISO8601 = function (string) {
    var regexp = "([0-9]{4})(-([0-9]{2})(-([0-9]{2})" +
        "(T([0-9]{2}):([0-9]{2})(:([0-9]{2})(\.([0-9]+))?)?" +
        "(Z|(([-+])([0-9]{2}):([0-9]{2})))?)?)?)?";
    var d = string.match(new RegExp(regexp));
    var offset = 0;
    var date = new Date(d[1], 0, 1);
    if (d[3]) { date.setMonth(d[3] - 1); }
    if (d[5]) { date.setDate(d[5]); }
    if (d[7]) { date.setHours(d[7]); }
    if (d[8]) { date.setMinutes(d[8]); }
    if (d[10]) { date.setSeconds(d[10]); }
    if (d[12]) { date.setMilliseconds(Number("0." + d[12]) * 1000); }
    if (d[14]) {
        offset = (Number(d[16]) * 60) + Number(d[17]);
        offset *= ((d[15] == '-') ? 1 : -1);
    }
    offset -= date.getTimezoneOffset();
    time = (Number(date) + (offset * 60 * 1000));
    this.setTime(Number(time));
}