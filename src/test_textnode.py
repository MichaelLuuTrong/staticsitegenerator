import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node1 = TextNode("This is a text node", TextType.NORMAL)
        node2 = TextNode("This is another text node", TextType.NORMAL)
        self.assertNotEqual(node1, node2)

    def test_not_eq2(self):
        node1 = TextNode("This is a text node", TextType.NORMAL)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_eq2(self):
        node1 = TextNode("This is a text node", TextType.LINK, "http://google.com")
        node2 = TextNode("This is a text node", TextType.LINK, "http://google.com")
        self.assertEqual(node1, node2)

if __name__ == "__main__":
    unittest.main()


