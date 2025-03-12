import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class testHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        testnode1 = HTMLNode("h1", "this is a header", None, {"href": "https://www.google.com", "target": "_blank",})
        testnode1_props_to_html = testnode1.props_to_html()
        self.assertEqual(testnode1_props_to_html, "href=https://www.google.com target=_blank")

    def test_repr_test(self):
        testnode1 = HTMLNode("h1", "this is a header", None, {"href": "https://www.google.com", "target": "_blank",})
        repr_return = testnode1.__repr__()
        self.assertEqual(repr_return, ("h1", "this is a header", None, {"href": "https://www.google.com", "target": "_blank",}))

    def test_props_to_html(self):
        testnode1 = HTMLNode("h2", "this is a smaller header", None, {"href": "https://boot.dev.com",})
        testnode1_props_to_html = testnode1.props_to_html()
        self.assertEqual(testnode1_props_to_html, "href=https://boot.dev.com")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Hello, world!")
        self.assertEqual(node.to_html(), "<h1>Hello, world!</h1>")
    
    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",)

    def test_to_html_without_chldren(self):
        with self.assertRaises(ValueError) as context:
            ParentNode("p", None)
        self.assertEqual(str(context.exception), "ParentNode must have children")

    def test_to_html_without_tag(self):
        child = LeafNode("b", "child")
        with self.assertRaises(ValueError) as context:
            ParentNode(None, child)
        self.assertEqual(str(context.exception), "ParentNode must have tag(s)")

    def test_to_html_with_multiple_children(self):
        node1 = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node1.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

