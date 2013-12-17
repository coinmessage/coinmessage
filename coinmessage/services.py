import urllib2
import json

def get_public_key_from_address(address):
    url = "https://blockchain.info/q/pubkeyaddr/%s" % address
    f = urllib2.urlopen(url)
    return f.read()
