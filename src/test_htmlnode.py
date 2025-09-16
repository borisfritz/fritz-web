import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_node_values(self):
        node = HTMLNode("p", "this is a paragraph!", None, None)
        self.assertEqual(
            node.tag,
            "p",
        )
        self.assertEqual(
            node.value,
            "this is a paragraph!",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )
        
    def test_props_to_html(self):
        props = {"href": "boot.dev", "src": "asset/image/suffer.jpg", "alt": "you will suffer in this class!"}
        node = HTMLNode(None, None, None, props)
        result = node.props_to_html()
        expected = ' href="boot.dev" src="asset/image/suffer.jpg" alt="you will suffer in this class!"'
        self.assertEqual(result, expected)

    def test_repr(self):
        node = HTMLNode("p", "What a strange world", None, {"class": "primary"})
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, None, {'class': 'primary'})",
        )
        
class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "link", {'href':'https://www.google.com'})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">link</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello World!")
        self.assertEqual(node.to_html(), 'Hello World!')

    def test_leaf_repr(self):
        node = LeafNode("b", "Bold Text Test!")
        self.assertEqual(node.__repr__(), "LeafNode(b, Bold Text Test!, None)")

if __name__ == "__main__":
    unittest.main()
