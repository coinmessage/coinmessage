import hashlib

from base64 import b64encode, b64decode

from encrypt import base58_to_privkey, pubhex_to_pubkey
from services import get_public_key_from_address

def encrypt_message(address, message):
    hex_public_key = get_public_key_from_address(address)
    public_key = pubhex_to_pubkey(hex_public_key)
    encrypted = b64encode(public_key.encrypt(message))
    return encrypted

def decrypt_message(b58_private_key, encrypted_message):
    private_key = base58_to_privkey(b58_private_key)
    return private_key.decrypt(b64decode(encrypted_message))
    

