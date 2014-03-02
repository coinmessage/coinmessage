import unittest

from Crypto.Random.random import randrange, long_to_bytes

from coinmessage.encrypt import PubKey, PrivKey


class EncryptionTest(unittest.TestCase):
    """Test using known public/private key pairs in bitcoin.
    Specifically, the private key with secret exponent 1.
    """

    def setUp(self):
        self.private_key = PrivKey(1)
        self.public_key = self.private_key.pubkey

    def test_address(self):
        self.assertEquals(self.public_key.__repr__(),
                          '1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH')

    def test_wif(self):
        self.assertEquals(
            self.private_key.__repr__(),
            'KwDiBf89QgGbjEhKnhXJuH7LrciVrZi3qYjgd9M7rFU73sVHnoWn')

    def test_encrypt_and_decrypt(self):
        s = long_to_bytes(randrange(2**1024))
        secret = self.public_key.encrypt(s)
        length = len(s)
        self.assertEquals(s, self.private_key.decrypt(secret)[:length])

    def test_invalid_decrypt(self):
        s = long_to_bytes(randrange(2**1024))
        secret = self.public_key.encrypt(s)
        with self.assertRaises(Exception):
            self.private_key.decrypt(secret[:-1])


if __name__ == '__main__':
    unittest.main()  # pragma: no cover
