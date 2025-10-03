import unittest

from src.block_markdown import BlockType
from src.block_markdown import markdown_to_blocks, get_blocktype, get_heading_tag, block_to_htmlnode
from src.htmlnode import ParentNode, LeafNode

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_extra_ws(self):
        md = """
this paragraph has extra whitespace after it!



   This paragraph has extra whitespace around it!   

 -this is a list with extra whitespace.
-this is not a list with extra whitespace.
- nothing should happen here except at the start and end of the block!   
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "this paragraph has extra whitespace after it!",
                "This paragraph has extra whitespace around it!",
                "-this is a list with extra whitespace.\n-this is not a list with extra whitespace.\n- nothing should happen here except at the start and end of the block!"
            ]
        )

class TestGetBlockType(unittest.TestCase):
    def test_get_blocktype_paragraph(self):
        block = "this is a paragraph of regular text!"
        block_type = get_blocktype(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_get_blocktype_heading(self):
        block = "### THIS IS A HEADING!"
        block_type = get_blocktype(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_get_blocktype_code(self):
        block = "```\n{this is}\na-bunch=of(code):\n```"
        block_type = get_blocktype(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_get_blocktype_quote(self):
        block = "> This is a quote\n> And this is a quote\n> This is also a quote!"
        block_type = get_blocktype(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_get_blocktype_unordered_list(self):
        block = "- cup\n- plate\n- silverware\n- bowl"
        block_type = get_blocktype(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_get_blocktype_ordered_list(self):
        block = "1. Number One\n2. Number Two\n3. Number Three\n4. Number Four"
        block_type = get_blocktype(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_get_blocktype_incorrect_ol(self):
        block = "1. Number One\n2. Number Two\n6. Number Three\n4. Number Four"
        block_type = get_blocktype(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_get_blocktype_incorrect_ul(self):
        block = "-cup\n-plate\nsilverware\n-bowl"
        block_type = get_blocktype(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

class TestGetHeadingTag(unittest.TestCase):
    def test_h1(self):
        block = "# heading"
        result = get_heading_tag(block)
        self.assertEqual(result, "h1")

    def test_h2(self):
        block = "## heading"
        result = get_heading_tag(block)
        self.assertEqual(result, "h2")

    def test_h3(self):
        block = "### heading"
        result = get_heading_tag(block)
        self.assertEqual(result, "h3")

    def test_h4(self):
        block = "#### heading"
        result = get_heading_tag(block)
        self.assertEqual(result, "h4")

    def test_h5(self):
        block = "##### heading"
        result = get_heading_tag(block)
        self.assertEqual(result, "h5")

    def test_h6(self):
        block = "###### heading"
        result = get_heading_tag(block)
        self.assertEqual(result, "h6")

class TestBlockToHTMLNode(unittest.TestCase):
    def test_heading_to_html(self):
        block = "### This is a heading!"
        node = block_to_htmlnode(block, BlockType.HEADING)
        result = node.to_html()
        self.assertEqual(result, "<h3>This is a heading!</h3>")

    def test_code_to_html(self):
        block = """
```
this is ( [ { a } ] ):
    a bunch of code:
    string = "string"
        **not markdown bold**
```
"""
        node = block_to_htmlnode(block, BlockType.CODE)
        result = node.to_html()
        self.assertEqual(result, '<pre><code>this is ( [ { a } ] ):\n    a bunch of code:\n    string = "string"\n        **not markdown bold**</code></pre>')

    def test_quote_to_html(self):
        block = """
> Quote line one
>
> and quote line two
"""
        node = block_to_htmlnode(block, BlockType.QUOTE)
        result = node.to_html()
        self.assertEqual(result, "<blockquote>Quote line one\n\nand quote line two</blockquote>")

    def test_ul_to_html(self):
        block = """
- item one
- item two
- item three
- item four
"""
        node = block_to_htmlnode(block, BlockType.UNORDERED_LIST)
        result = node.to_html()
        self.assertEqual(result, "<ul><li>item one</li><li>item two</li><li>item three</li><li>item four</li></ul>")

    def test_ul_to_html_with_bold(self):
        block = """
- item one
- item **two**
- item three
- item four
"""
        node = block_to_htmlnode(block, BlockType.UNORDERED_LIST)
        result = node.to_html()
        self.assertEqual(result, "<ul><li>item one</li><li>item <b>two</b></li><li>item three</li><li>item four</li></ul>")

    def test_ol_to_html(self):
        block = """
1. item one
2. item two
3. item three
4. item four
"""
        node = block_to_htmlnode(block, BlockType.ORDERED_LIST)
        result = node.to_html()
        self.assertEqual(result, "<ol><li>item one</li><li>item two</li><li>item three</li><li>item four</li></ol>")

    def test_ol_to_html(self):
        block = """
1. item one
2. item **two**
3. item three
4. item four
"""
        node = block_to_htmlnode(block, BlockType.ORDERED_LIST)
        result = node.to_html()
        self.assertEqual(result, "<ol><li>item one</li><li>item <b>two</b></li><li>item three</li><li>item four</li></ol>")

    def test_invalid_blocktype(self):
        with self.assertRaises(AttributeError):
            node = block_to_htmlnode("block", BlockType.UNK)

    def test_paragraph_to_htmlnode(self):
        block = "This is another paragraph with _italic_ text and `code` here"
        html_node = block_to_htmlnode(block, BlockType.PARAGRAPH)
        result = html_node.to_html()
        self.assertEqual(result, "<p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p>")

