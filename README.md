Coin Message
=========

The [Coin Message](https://github.com/coinmessage/coinmessage) project is a secure messaging client written in Python. It uses the Bitcoin blockchain to get public keys necessary for encrypting using elliptical curve cryptography.

Overview of Coin Messaging
------------

Secure messaging already exists with protocols like PGP. Unfortunately, the discovery of public keys is somewhat problematic unless supplied by the actual person. This problem is known in cryptography circles as the Public Key Infrastructure (PKI) problem. Bitcoin elegantly solves this by making the public keys available in the blockchain.

Mechanics
-----------

The mechanics of coin messaging are pretty straightforward.

Let e = secret exponent and p = g ^ e, where g is the base point for the elliptical curve. e is the private key and p is the public key. To encrypt a message using the public key, let n be some nonce used for encryption known by the message sender. p ^ n represents the shared secret. That shared secret is used for encrypting a message to the owner of the public key. The message is sent with g ^ n, which the private key can use to derive p ^ n since p ^ n = (g ^ n) ^ e. Thus, the shared secret can be communicated to the private key owner safely as either n or e have to be known by an attacker to figure out p ^ n. As neither are transmitted and cannot easily be derived from g ^ n, the message is secure.

Usage
-----------

Note the address needs to have spent money in order to be able to send/receive messages to/from it. If you already have an address in your bitcoind wallet, you don't need to do the first step.

    $ bitcoind importprivkey KwDiBf89QgGbjEhKnhXJuH7LrciVrZi3qYjgd9M7rFU73sVHnoWn
    $ ./send 1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH "secret message"
    AvxxqJiQ840M4/tmIVKFFwlxNRuzZDirbn20MqS3oCtTYUUZdsyWkTRCagab7NvUEl1U1DyK47dYHqkcThiPjdw=
    $ ./receive 1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH AvxxqJiQ840M4/tmIVKFFwlxNRuzZDirbn20MqS3oCtTYUUZdsyWkTRCagab7NvUEl1U1DyK47dYHqkcThiPjdw=

Dependencies
------------

* [pycoin](https://github.com/richardkiss/pycoin) is used for ECC math
* [pycrypto](https://github.com/dlitz/pycrypto) is used for AES encryption


Contributors
------------

 * Jimmy Song

License
-------

MIT (see LICENSE file)

Donations
---------

To financially support this project you can donate to this Bitcoin address: 15vNKVvD9PGrbCWvgwUDnQs1rk1YFkjLJT.
