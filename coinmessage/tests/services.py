import unittest

from coinmessage.services import get_public_key_from_address

class ServicesTest(unittest.TestCase):

    def setUp(self):
        self.pub_string = "04588d202afcc1ee4ab5254c7847ec25b9a135bbda0f2bc69ee1a714749fd77dc9f88ff2a00d7e752d44cbe16e1ebcf0890b76ec7c78886109dee76ccfc8445424"
        self.address = "1CC3X2gu58d6wXUWMffpuzN9JAfTUWu4Kj"

    def test_address(self):
        pub_string = get_public_key_from_address(self.address)
        self.assertEquals(pub_string, self.pub_string)

