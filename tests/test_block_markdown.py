import unittest

from src.block_markdown import markdown_to_blocks, block_to_blocktype, BlockType

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

    ### BLOCK TO BLOCKTYPE ###

    def test_block_to_blocktype_paragraph(self):
        block = "this is a paragraph of regular text!"
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_blocktype_heading(self):
        block = "### THIS IS A HEADING!"
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_blocktype_code(self):
        block = "```\n{this is}\na-bunch=of(code):\n```"
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_blocktype_quote(self):
        block = "> This is a quote\n> And this is a quote\n> This is also a quote!"
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_blocktype_unordered_list(self):
        block = "- cup\n- plate\n- silverware\n- bowl"
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_to_blocktype_ordered_list(self):
        block = "1. Number One\n2. Number Two\n3. Number Three\n4. Number Four"
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_block_to_blocktype_incorrect_ol(self):
        block = "1. Number One\n2. Number Two\n6. Number Three\n4. Number Four"
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_blocktype_incorrect_ul(self):
        block = "-cup\n-plate\nsilverware\n-bowl"
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

