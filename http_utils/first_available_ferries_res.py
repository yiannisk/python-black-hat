import json
import urllib2

base_url = 'http://ferries-v1.production.api.e-travel.gr/reservations/'

f = open('ferries_reservation_ids.txt', 'r')

for line in f:
	id = "".join(line.split())
	print "Testing [%s]" % id
	request = urllib2.Request(base_url+id)
	request.add_header('Accept', 'application/json')
	data = json.load(urllib2.urlopen(request))
	print data["Status"]
	if data["Status"] == "Success":
		print "Done. Successful reservation located is [%s]" % id
		break;
