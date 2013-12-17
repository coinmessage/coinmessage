import unittest
import os

from encrypt import EncryptionTest
from services import ServicesTest

from coinmessage import encrypt_message, decrypt_message

class MainTest(unittest.TestCase):

    def setUp(self):
        self.address = "1CC3X2gu58d6wXUWMffpuzN9JAfTUWu4Kj"
        self.priv_string = '5Kb8kLf9zgWQnogidDA76MzPL6TsZZY36hWXMssSzNydYXYB9KF'

    def test_encrypt_decrypt(self):
        s = os.urandom(500)
        encrypted_message = encrypt_message(self.address, s)
        message = decrypt_message(self.priv_string, encrypted_message)
        self.assertEqual(s, message)

