import unittest

from src.inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_image_link, split_nodes_link, text_to_textnodes
from src.textnode import TextNode, TextType

### split_nodes_delimiter testing ###

class TestSplitNodes(unittest.TestCase):
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

    def test_unclosed_delimiter(self):
        node = [TextNode("Some **bold text!", TextType.TEXT)]
        with self.assertRaises(Exception):
            result = split_nodes_delimiter(node, "**", TextType.TEXT)

### EXTRACT MARKDOWN TESTING ###

    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

### IMAGE TEXT SPLITTING ###

    def test_split_image(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_link(self):
        node = TextNode("This is text with an [![image](https://i.imgur.com/zjjcJKZ.png)](https://google.com)", TextType.TEXT)
        new_nodes = split_nodes_image_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image||LINK||https://google.com", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode("![image](https://www.example.COM/IMAGE.PNG)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
            ],
            new_nodes,
        )

    def test_split_image_no_image(self):
        node = [TextNode("There is no image text here!", TextType.TEXT)]
        result = split_nodes_image(node)
        self.assertEqual(result, node)

    ### LINK TEXT SPLITTING ###

    def test_split_links(self):
        node = TextNode("This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and a [second link](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png")
            ],
            new_nodes,
        )
    
    ### RAW TEXT INPUT TO TEXT NODES ###

    def test_mixed_inline_elements(self):
        text = (
            "This is **text** with an _italic_ word and a `code ** block` "
            "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code ** block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(nodes, expected)

    def test_plain_text(self):
        text = "just plain words"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [TextNode("just plain words", TextType.TEXT)])

    def test_unmatched_delimiters_no_change(self):
        text = "this has **unmatched and _also unmatched"
        with self.assertRaises(Exception):
            nodes = text_to_textnodes(text)
