#!/usr/bin/env python

#   author: Arran Gallagher <arrangallagher@gmail.com>
#  created: 2011-03-27
# modified: 2011-03-30

import dns.name
import dns.resolver
import httplib
import base64
import sys

def noip_lookup(hostname):
        parent_domain = dns.name.from_text(hostname).parent()
        dns_response = dns.resolver.query(parent_domain, 'SOA')
        if len(dns_response) > 0:
                dns_response = dns.resolver.query(dns_response[0].mname, 'A')
		if len(dns_response) > 0:
			resolver = dns.resolver.Resolver('', False)
			resolver.nameservers = [dns_response[0].address]
			dns_response = resolver.query(hostname, 'A')
			if len(dns_response) > 0:
				return dns_response[0].address
			
NOIP_USERNAME = ''
NOIP_PASSWORD = ''
NOIP_HOSTNAME = ''
NOIP_IPADDRESS = sys.argv[1]

if noip_lookup(NOIP_HOSTNAME) == NOIP_IPADDRESS:
	sys.exit()


HTTP_METHOD = 'GET'
HTTP_HOST = 'dynupdate.no-ip.com'
HTTP_URL = '/nic/update?hostname=%s&myip=%s'
HTTP_USER_AGENT = 'Arrans noip-update arrangallagher@gmail.com'
HTTP_BASIC_AUTH = 'Basic %s' 

HTTP_BASIC_AUTH %= base64.b64encode(NOIP_USERNAME + ':' + NOIP_PASSWORD)
HTTP_URL %= (NOIP_HOSTNAME, NOIP_IPADDRESS) 

con = httplib.HTTPConnection(HTTP_HOST)
con.putrequest(HTTP_METHOD, HTTP_URL)
con.putheader('User-Agent', HTTP_USER_AGENT)
con.putheader('Authorization', HTTP_BASIC_AUTH)
con.endheaders()

res = con.getresponse()
print res.read()
