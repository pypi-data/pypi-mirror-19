# -*- coding: utf-8 -*-
import unittest
from tag_processor import DataContainer


class TagParserTest(unittest.TestCase):

    def test_str(self):
        data = DataContainer()
        self.assertEqual("[1, 2, 3]", data.str([1, 2, 3]))
        self.assertEqual(None, data.str(None))

    def test_join(self):
        data = DataContainer()
        self.assertEqual("You, Me, and You", data.join(None, ", ", None, "You", "", "Me", "and You"))

    def test_wrap(self):
        data = DataContainer()
        self.assertEqual("(really?)", data.wrap(None, "(", "really?", ")"))
        self.assertEqual(None, data.wrap(None, "(", None, ")"))
        self.assertEqual(None, data.wrap(None, "(", "", ")"))
