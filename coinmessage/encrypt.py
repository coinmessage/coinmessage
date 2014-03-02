import hashlib
import hmac

from Crypto.Cipher import AES
from Crypto.Random.random import randrange

from pycoin.encoding import (
    public_pair_to_bitcoin_address, public_pair_to_sec,
    sec_to_public_pair, secret_exponent_to_wif)

from pycoin.ecdsa import Point, generator_secp256k1 as BasePoint


class PubKey(Point):
    """Represents the public key. Subclasses the pycoin.ecdsa's Point
    and adds several useful methods
    """
    def address(self):
        """Returns the well-known base58 bitcoin address for this PubKey"""
        return public_pair_to_bitcoin_address((self.x(), self.y()))

    def encrypt(self, s, mac=16):
        """Encrypt a message for private viewing by the holder of the
        Private Key
        """
        # nonce is essentially a secret on the encrypter's side
        # this is a secret exponent < 2^256
        nonce = randrange(1, self.curve().p())
        tmp = BasePoint * nonce
        nonce_point = PubKey(tmp.curve(), tmp.x(), tmp.y())
        tmp = self * nonce
        shared_secret = PubKey(tmp.curve(), tmp.x(), tmp.y())

        # derive a key for making a cipher and checksum using the
        # nonce point and shared secret
        key = nonce_point.kdf(shared_secret)

        # encode the nonce point into the message as the beginning
        header = nonce_point.sec()

        # encrypt the actual message using the AES cipher
        cipher = AES.new(key[:32])
        # because we're using AES block mode, we need multiples of 16
        s = s + '\x00' * (16 - len(s) % 16)
        message = cipher.encrypt(s)

        # add a checksum for validation
        checksum_maker = hmac.new(key[32:], digestmod=hashlib.sha256)
        checksum_maker.update(message)
        checksum = checksum_maker.digest()[:mac]
        return header + message + checksum

    def kdf(self, another_p):
        """Simple Key-Derivative Function given two numbers"""
        return hashlib.sha512(self.sec() + another_p.sec()).digest()

    def sec(self):
        """Take a point on the curve and encode it into sec format (33 bytes)
        """
        return public_pair_to_sec((self.x(), self.y()))

    def __repr__(self):
        return self.address()


class PrivKey:
    """Represents the private key (secret exponent) for Elliptical Curve
    Cryptography
    """
    def __init__(self, exponent):
        self.exponent = exponent
        point = BasePoint * exponent
        self.pubkey = PubKey(point.curve(), point.x(), point.y())

    def wif(self, compressed=True):
        """Return the base58 representation (WIF format) for the private
        key
        """
        return secret_exponent_to_wif(self.exponent)

    def decrypt(self, raw, mac=16):
        """Decrypt a message sent to the holder of this key.
        """
        # get the nonce-point
        x, y = sec_to_public_pair(raw[:33])
        # validation that this point lies on the curve happens in
        #  initialization
        nonce_point = PubKey(BasePoint.curve(), x, y)

        # message gives us the ciphered message
        message = raw[33:-mac]
        # checksum makes sure everything is transmitted properly
        checksum = raw[-mac:]

        # calculate the shared secret
        tmp = nonce_point * self.exponent
        shared_secret = PubKey(tmp.curve(), tmp.x(), tmp.y())

        # derive keys
        key = nonce_point.kdf(shared_secret)
        cipher = AES.new(key[:32])

        # verify the checksum
        checksum_maker = hmac.new(key[32:], digestmod=hashlib.sha256)
        checksum_maker.update(message)
        if checksum_maker.digest()[:mac] != checksum:
            raise RuntimeError("Invalid checksum on encoded message string")

        return cipher.decrypt(message)

    def __repr__(self):
        return self.wif()
