import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.LINK, url="google.com")
        node2 = TextNode("This is a text node", TextType.LINK, url="google.com")
        self.assertEqual(node, node2)

    def test_ne_text(self):
        node = TextNode("This is some text", TextType.TEXT)
        node2 = TextNode("This is some text!", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_ne_type(self):
        node = TextNode("This is some text", TextType.ITALIC)
        node2 = TextNode("This is some text", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_ne_url1(self):
        node = TextNode("This is some text", TextType.LINK, url="google.com")
        node2 = TextNode("This is some text", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_ne_url2(self):
        node = TextNode("This is some text", TextType.TEXT, url="google.com")
        node2 = TextNode("This is some text", TextType.TEXT, url="boot.dev")
        self.assertNotEqual(node, node2)

    def test_ne_all(self):
        node = TextNode("This is some text!", TextType.TEXT)
        node2 = TextNode("This is some text", TextType.LINK, url="boot.dev")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
