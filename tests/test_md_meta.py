import unittest
from src.md_meta import extract_title

class TestExtractTitle(unittest.TestCase):

    def test_basic_h1(self):
        md = "# Hello World"
        self.assertEqual(extract_title(md), "Hello World")

    def test_h1_with_whitespace(self):
        md = "#    My Title   "
        self.assertEqual(extract_title(md), "My Title")

    def test_h1_not_first_line(self):
        md = "\nSome intro text\n# My Title\nMore text"
        self.assertEqual(extract_title(md), "My Title")

    def test_no_h1_raises(self):
        md = "## Subheading\nSome text here"
        with self.assertRaises(ValueError):
            extract_title(md)

    def test_multiple_h1s_returns_first(self):
        md = "# First Title\n# Second Title"
        self.assertEqual(extract_title(md), "First Title")

if __name__ == "__main__":
    unittest.main()