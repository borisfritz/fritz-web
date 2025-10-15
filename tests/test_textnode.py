import unittest

from src.textnode import TextNode, TextType, text_node_to_html_node

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

### TEXT_TO_HTML_NODE TESTS ###

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, url="google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href":"google.com"})

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, url="image/test.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src":"image/test.jpg", "alt":"This is an image node"})

    def test_image_link(self):
        node = TextNode("This is an image-link node||LINK||google.com", TextType.IMAGE, url="image/test.jpg")
        html_node = text_node_to_html_node(node)
        result = html_node.to_html()
        self.assertEqual(result, '<a href="google.com"><img src="image/test.jpg" alt="This is an image-link node"></img></a>')

    def test_invalid_text_node(self):
        with self.assertRaises(AttributeError):
            node = TextNode("text", TextType.NONE)

    def test_invalid_text_node_to_html_node_text_type(self):
        with self.assertRaises(ValueError):
            text_node_to_html_node(TextNode("text", "???"))


if __name__ == "__main__":
    unittest.main()
