#!/usr/bin/env python

import sys

from coinmessage import encrypt_message


USAGE = """%s <bitcoin address> <message>""" % sys.argv[0]

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(USAGE)

    bitcoin_address, message = sys.argv[1:]

    if len(bitcoin_address) != 34:
        sys.exit(USAGE)

    print encrypt_message(bitcoin_address, message)
