import unittest

from src.htmlnode import HTMLNode, LeafNode, ParentNode

### HTMLNODE TESTS ###

class TestHTMLNode(unittest.TestCase):
    def test_node_values(self):
        node = HTMLNode("p", "this is a paragraph!", ["list"], {"key":"value"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "this is a paragraph!")
        self.assertEqual(node.children, ["list"])
        self.assertEqual(node.props, {"key":"value"})
        
    def test_not_implemented(self):
        node = HTMLNode("p", "paragraph", None, None)
        with self.assertRaises(NotImplementedError):
            node.to_html() 

    def test_props_to_html(self):
        props = {"href": "boot.dev", "src": "asset/image/suffer.jpg", "alt": "you will suffer in this class!"}
        node = HTMLNode(None, None, None, props)
        result = node.props_to_html()
        expected = ' href="boot.dev" src="asset/image/suffer.jpg" alt="you will suffer in this class!"'
        self.assertEqual(result, expected)

    def test_empty_props_to_html(self):
        props = None
        node = HTMLNode(None, None, None, props)
        result = node.props_to_html()
        expected = ""
        self.assertEqual(result, expected)

    def test_repr(self):
        node = HTMLNode("p", "What a strange world", None, {"class": "primary"})
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, None, {'class': 'primary'})",
        )

### LEAFNODE TESTS ###       

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_empty_props(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "link", {'href':'https://www.google.com'})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">link</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello World!")
        self.assertEqual(node.to_html(), 'Hello World!')

    def test_leaf_repr(self):
        node = LeafNode("b", "Bold Text Test!")
        self.assertEqual(node.__repr__(), "LeafNode(b, Bold Text Test!, None)")

### PARENTNODE TESTS ###

class TestParentNode(unittest.TestCase):
    def test_to_html_with_child(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_children(self):
        child_nodes = [
            LeafNode("span", "child"),
            LeafNode("p","paragraph"),
            LeafNode("b", "bold"),
            LeafNode(None, "text"),
            LeafNode("a", "link", {"href":"google.com"})
        ]
        parent_node = ParentNode("div", child_nodes)
        self.assertEqual(parent_node.to_html(), '<div><span>child</span><p>paragraph</p><b>bold</b>text<a href="google.com">link</a></div>')

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_no_tag_value(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("p", "paragraph")]).to_html()

    def test_parent_no_child_value(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()

    def test_parent_repr(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.__repr__(), 'ParentNode(div, [LeafNode(span, child, None)], None)')

if __name__ == "__main__":
    unittest.main()
