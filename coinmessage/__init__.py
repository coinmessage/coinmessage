import hashlib

from base64 import b64encode, b64decode
from pycoin.encoding import sec_to_public_pair, wif_to_secret_exponent
from encrypt import PubKey, PrivKey, BasePoint
from services import get_public_key_from_address, get_private_key_from_address


def encrypt_message(address, message):
    """Encrypts a message to an address.
    """
    hex_public_key = get_public_key_from_address(address)
    x, y = sec_to_public_pair(hex_public_key.decode('hex'))
    public_key = PubKey(BasePoint.curve(), x, y)
    encrypted = b64encode(public_key.encrypt(message))
    return encrypted


def decrypt_message(public_key, encrypted_message):
    """Decrypts the message given a public key and an encrypted message.
    User needs to control the private key via bitcoind.
    """
    wif = get_private_key_from_address(public_key)
    secret_exponent = wif_to_secret_exponent(wif)
    private_key = PrivKey(secret_exponent)
    return private_key.decrypt(b64decode(encrypted_message))
