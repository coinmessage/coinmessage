import json
import subprocess
import urllib2


def get_public_key_from_address(address):
    """Read the public key for an address using blockchain.info
    """
    url = "https://blockchain.info/q/pubkeyaddr/%s" % address
    f = urllib2.urlopen(url)
    s = f.read()
    if len(s) < 1:
        raise RuntimeError("Public Key does not seem to be in the blockchain")
    return s


def get_private_key_from_address(address):
    """Read the private key for an address you control using bitcoind
    """
    p = subprocess.Popen(['bitcoind', 'dumpprivkey', address],
                         stdout=subprocess.PIPE)
    out, err = p.communicate()
    return out.strip()
