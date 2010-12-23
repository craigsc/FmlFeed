#!/usr/bin/env python
from tornado import httpclient
from tornado import escape
import memcache

client = httpclient.HTTPClient()
try:
	response = client.fetch("https://graph.facebook.com/search?q=fml&type=post&limit=50")
	json = escape.json_decode(response.body)
	mc = memcache.Client(['127.0.0.1:11211'], debug=0)
	mc.set("newest", json)
except httpclient.HTTPError, e:
	# bad things happen so don't do anything, just try again on next cron
	print "error"