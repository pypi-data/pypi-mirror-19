from unittest import TestCase
from millibot import MilliBot

class MilliBotTests(TestCase):

    def setUp(self):
        self.millibot = MilliBot('Awesome Bot')

    def test_get_response(self):
        self.assertEqual(self.millibot.get_response('Hi'), 'Hi')
