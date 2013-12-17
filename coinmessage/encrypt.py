import hashlib
import hmac

from Crypto.Cipher import AES
from Crypto.Random.random import randrange, long_to_bytes, bytes_to_long
from Crypto.Util import Counter

from pycoin.encoding import a2b_base58, b2a_hashed_base58, hash160
from pycoin.ecdsa import (
    Point, public_pair_for_x, generator_secp256k1 as BasePoint)


def make_cipher(h):
    """Initialize an AES cipher for encrypting/decrypting"""
    return AES.new(h, AES.MODE_CTR, counter=Counter.new(128, initial_value=0))


def kdf(p1,p2):
    return hashlib.sha512(to_bytes(p1) + to_bytes(p2)).digest()


def to_bytes(p):
    # encode the point into 34 bytes
    x, parity = p.x(), p.y() % 2
    return long_to_bytes(parity, 2) + long_to_bytes(x, 32)


def valid(point):
    p, a, b = point.curve().p(), point.curve().a(), point.curve().b()
    x, y = point.x(), point.y()

    # y^2 = x^3 + ax + b mod m is true
    return (y ** 2) % p == (x ** 3 + a * x + b) % p


class PubKey(Point):
    def address(self, prefix="\x00"):
        binary = long_to_bytes(self.x()) + long_to_bytes(self.y())
        return b2a_hashed_base58(prefix + hash160("\x04" + binary))

    def encrypt(self, s, mac=8):
        """Encrypt a message for private viewing by the holder of the
        Private Key
        """
        nonce = randrange(1, self.curve().p())
        nonce_point = BasePoint * nonce
        shared_secret = self * nonce
        key = kdf(nonce_point, shared_secret)
        header = to_bytes(nonce_point)
        cipher = make_cipher(key[:32])
        message = cipher.encrypt(s)
        checksum_maker = hmac.new(key[32:], digestmod=hashlib.sha256)
        checksum_maker.update(message)
        checksum = checksum_maker.digest()[:mac]
        return header + message + checksum


class PrivKey:
    def __init__(self, exponent):
        self.exponent = exponent
        self.pubkey = BasePoint * exponent

    def b58(self, prefix="\x80"):
        return b2a_hashed_base58(prefix + long_to_bytes(self.exponent, 32))

    def decrypt(self, raw, mac=8):
        """Decrypt a message sent to the holder of this key.
        """
        parity = bytes_to_long(raw[0:2])
        header = raw[2:34]
        message = raw[34:-mac]
        checksum = raw[-mac:]
        x, y = public_pair_for_x(BasePoint, bytes_to_long(header), not parity)
        nonce_point = Point(BasePoint.curve(),x,y)
        assert valid(nonce_point)
        shared_secret = nonce_point * self.exponent
        key = kdf(nonce_point, shared_secret)
        cipher = make_cipher(key[:32])
        # verify the checksum
        checksum_maker = hmac.new(key[32:], digestmod=hashlib.sha256)
        checksum_maker.update(message)
        if checksum_maker.digest()[:mac] != checksum:
            raise Exception

        return cipher.decrypt(message)

def base58_to_privkey(b58):
    # the first byte is the identifier and the last 4 is the checksum
    e = bytes_to_long(a2b_base58(b58)[1:-4])
    return PrivKey(e)

def pubhex_to_pubkey(h):
    s = h.decode('hex')
    if s[0] != '\x04':
        raise Exception("invalid public hex")
    s = s[1:]
    x = bytes_to_long(s[:32])
    y = bytes_to_long(s[32:])
    return PubKey(BasePoint.curve(),x,y)


