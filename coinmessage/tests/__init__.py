import unittest
import os

from encrypt import EncryptionTest
from services import ServicesTest

from coinmessage import encrypt_message, decrypt_message


class MainTest(unittest.TestCase):

    def setUp(self):
        self.address = "1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH"

    def test_encrypt_decrypt(self):
        s = os.urandom(500)
        length = len(s)
        encrypted_message = encrypt_message(self.address, s)
        message = decrypt_message(self.address, encrypted_message)
        self.assertEqual(s, message[:length])


if __name__ == '__main__':
    unittest.main()
