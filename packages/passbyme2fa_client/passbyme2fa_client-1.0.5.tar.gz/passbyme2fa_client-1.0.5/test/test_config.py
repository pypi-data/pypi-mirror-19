from passbyme2fa_client import *
import unittest

class TestConfig(unittest.TestCase):

    def test_should_miss_key(self):
        with self.assertRaises(ValueError):
            PassByME2FAClient()

    def test_should_miss_cert(self):
        with self.assertRaises(ValueError):
            PassByME2FAClient(key = "Given")
