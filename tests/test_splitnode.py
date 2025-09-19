import unittest

from src.split_node import split_nodes_delimiter
from src.textnode import TextNode, TextType

### split_nodes_delimiter testing ###

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_text_node_split(self):
        node = [TextNode("This is an _example_ of italic text!", TextType.TEXT)]
        result = split_nodes_delimiter(node, "_", TextType.ITALIC)
        expected = [TextNode("This is an ", TextType.TEXT, None), TextNode("example", TextType.ITALIC, None), TextNode(" of italic text!", TextType.TEXT, None)]
        self.assertEqual(result, expected)

    def test_bold_node(self):
        node = [TextNode("bold text", TextType.BOLD)]
        result = split_nodes_delimiter(node, "**", TextType.BOLD)
        expected = [TextNode("bold text", TextType.BOLD, None)]
        self.assertEqual(result, expected)
    
    def test_italic_node(self):
        node = [TextNode("italic text", TextType.ITALIC)]
        result = split_nodes_delimiter(node, "_", TextType.ITALIC)
        expected = [TextNode("italic text", TextType.ITALIC, None)]
        self.assertEqual(result, expected)

    def test_code_node(self):
        node = [TextNode("code text", TextType.CODE)]
        result = split_nodes_delimiter(node, "`", TextType.CODE)
        expected = [TextNode("code text", TextType.CODE, None)]
        self.assertEqual(result, expected)

    def test_text_node_split_no_extra_text(self):
        node = [TextNode("**Bold Text**", TextType.TEXT)]
        result = split_nodes_delimiter(node, "**", TextType.BOLD)
        expected = [TextNode("Bold Text", TextType.BOLD, None)]
        self.assertEqual(result, expected)

    def test_text_node_split_at_end(self):
        node = [TextNode("There is nothing after this **Bold Text**", TextType.TEXT)]
        result = split_nodes_delimiter(node, "**", TextType.BOLD)
        expected = [TextNode("There is nothing after this ", TextType.TEXT), TextNode("Bold Text", TextType.BOLD, None)]
        self.assertEqual(result, expected)

    def test_node_list(self):
        node = [
            TextNode("This is some **text!**", TextType.TEXT),
            TextNode("**This** is some text!", TextType.TEXT),
            TextNode("**Look at all of this bold!**", TextType.TEXT)
        ]
        result = split_nodes_delimiter(node, "**", TextType.BOLD)
        expected = [
            TextNode("This is some ", TextType.TEXT, None),
            TextNode("text!", TextType.BOLD, None),
            TextNode("This", TextType.BOLD, None),
            TextNode(" is some text!", TextType.TEXT, None),
            TextNode("Look at all of this bold!", TextType.BOLD, None),
        ]
        self.assertEqual(result, expected)

    def test_invalid_delimiter(self):
        node = [TextNode("Some **bold** text!", TextType.TEXT)]
        with self.assertRaises(ValueError):
            result = split_nodes_delimiter(node, "&", TextType.TEXT)

    def test_unclosed_delimiter(self):
        node = [TextNode("Some **bold text!", TextType.TEXT)]
        with self.assertRaises(Exception):
            result = split_nodes_delimiter(node, "**", TextType.TEXT)



