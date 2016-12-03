# -*- coding: utf-8

import unittest
import unke


class LexTest(unittest.TestCase):
    def test_comment_no_end(self):
        unke_text = """
            Root {
            /*
            }
            // Comment has no end
        """
        with self.assertRaises(unke.ParseException):
            unke.loads(unke_text)

    def test_illegal_character(self):
        unke_text = """
            Root {
                :D  // Raises ParseException(illegal character)
            }
        """
        with self.assertRaises(unke.ParseException):
            unke.loads(unke_text)
