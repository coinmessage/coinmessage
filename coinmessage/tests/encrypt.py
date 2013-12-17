import unittest

from Crypto.Random.random import randrange, long_to_bytes

from coinmessage.encrypt import pubhex_to_pubkey, base58_to_privkey

class EncryptionTest(unittest.TestCase):

    def setUp(self):
        self.pub_string = "04588d202afcc1ee4ab5254c7847ec25b9a135bbda0f2bc69ee1a714749fd77dc9f88ff2a00d7e752d44cbe16e1ebcf0890b76ec7c78886109dee76ccfc8445424"
        self.priv_string = '5Kb8kLf9zgWQnogidDA76MzPL6TsZZY36hWXMssSzNydYXYB9KF'

    def test_address(self):
        pub = pubhex_to_pubkey(self.pub_string)
        self.assertEquals(pub.address(), "1CC3X2gu58d6wXUWMffpuzN9JAfTUWu4Kj")

    def test_b58(self):
        priv = base58_to_privkey(self.priv_string)
        self.assertEquals(priv.b58(), self.priv_string)

    def test_encrypt_and_decrypt(self):
        s = long_to_bytes(randrange(2**1024))
        pub = pubhex_to_pubkey(self.pub_string)
        secret = pub.encrypt(s)
        priv = base58_to_privkey(self.priv_string)
        self.assertEquals(s, priv.decrypt(secret))

    def test_pubhex_to_pubkey(self):
        with self.assertRaises(Exception):
            pubhex_to_pubkey('111110')

    def test_invalid_decrypt(self):
        s = long_to_bytes(randrange(2**1024))
        pub = pubhex_to_pubkey(self.pub_string)
        secret = pub.encrypt(s)
        priv = base58_to_privkey(self.priv_string)
        with self.assertRaises(Exception):
            priv.decrypt(secret[:-1])
