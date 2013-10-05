import unittest

from quizfactory import utils


class TestIdentation(unittest.TestCase):

    def test_strip(self):
        strip = utils.strip_indents

        self.assertEqual(strip("test"), "test")
        self.assertEqual(strip("test\n\rtest"), "test\ntest")
        self.assertEqual(strip("test\n  \ntest"), "test\n\ntest")
        self.assertEqual(strip("\ttest\ntest"), "    test\ntest")
        self.assertEqual(strip("test\n\ttest"), "test\n    test")
        self.assertEqual(strip("\ttest\n\ttest"), "test\ntest")
        self.assertEqual(strip("test\t\t"), "test        ")
        self.assertEqual(strip("  test"), "test")

    def test_tab_to_space(self):
        strip = utils.strip_indents

        self.assertEqual(strip("test\ttest"), "test    test")
        self.assertEqual(strip("test\ttest", 1), "test test")
