import unittest
from markdown import *

class TestMarkdown(unittest.TestCase):
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
    def test_block_to_block_type_heading(self):
        block = "# HEADING"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.HEADING
        )
    def test_block_to_block_type_heading2(self):
        block = "## HEADING"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.HEADING
        )
    def test_block_to_block_type_heading3(self):
        block = "### HEADING"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.HEADING
        )
    def test_block_to_block_type_paragraph(self):
        block = "######## not a heading"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )
    def test_block_to_block_type_paragraph2(self):
        block = "paragraph"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )
    def test_block_to_block_type_quote(self):
        block = ">test\n>testrandomtext\n>moretext"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE
        )
    def test_block_to_block_type_unordered_list(self):
        block = "- test\n- testrandomtext\n- moretext"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.UNORDERED_LIST
        )
    def test_block_to_block_type_unordered_list(self):
        block = "- test\n- testrandomtext\n- moretext"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.UNORDERED_LIST
        )
    def test_block_to_block_type_ordered_list2(self):
        block = "1. test\n2. testrandomtext\n3.  moretext"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.ORDERED_LIST
        )
    def test_block_to_block_type_not_ordered_list(self):
        block = "2. test\n2. testrandomtext\n3. moretext"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )
    def test_block_to_block_type_not_ordered_list2(self):
        block = "1. test\n2. testrandomtext\n2. moretext"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )
if __name__ == "__main__":
    unittest.main()