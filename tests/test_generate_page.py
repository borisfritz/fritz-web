import unittest

from src.generate_page import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        md = "# test title!\n\nThis is the rest of the .md file!"
        result = extract_title(md)
        self.assertEqual(result, "test title!")
