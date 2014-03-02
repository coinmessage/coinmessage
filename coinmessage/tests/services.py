import unittest

from coinmessage.services import (get_public_key_from_address,
                                  get_private_key_from_address)


class ServicesTest(unittest.TestCase):

    def setUp(self):
        self.pub_string = "04588d202afcc1ee4ab5254c7847ec25b9a135bbda0f2bc" \
            "69ee1a714749fd77dc9f88ff2a00d7e752d44cbe16e1ebcf0890b76ec7c78" \
            "886109dee76ccfc8445424"
        self.address = "1CC3X2gu58d6wXUWMffpuzN9JAfTUWu4Kj"

    def test_address(self):
        pub_string = get_public_key_from_address(self.address)
        self.assertEquals(pub_string, self.pub_string)

    def test_address_fail(self):
        with self.assertRaises(RuntimeError):
            get_public_key_from_address("17uUag1hS4GX7KQync4Jt3ufNS9926Axpk")

    def test_private_key(self):
        address = "1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH"
        priv = get_private_key_from_address(address)
        self.assertEquals(
            priv, "KwDiBf89QgGbjEhKnhXJuH7LrciVrZi3qYjgd9M7rFU73sVHnoWn")


if __name__ == '__main__':
    unittest.main()  # pragma: no cover
