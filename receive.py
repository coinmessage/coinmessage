#!/usr/bin/env python

import sys

from coinmessage import decrypt_message


USAGE = """%s <public key with private key in bitcoind> <message>""" \
    % sys.argv[0]

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(USAGE)

    public_key, message = sys.argv[1:]

    if len(public_key) != 34:
        sys.exit(USAGE)

    print decrypt_message(public_key, message)
