import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links


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

    def test_normal(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_italic(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")

    def test_code(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")

    def test_link(self):
        node = TextNode("This is a link text node", TextType.LINK, "http://youtube.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link text node")
        self.assertEqual(html_node.props, {"href": "http://youtube.com"})

    def test_image(self):
        node = TextNode("This is an image text node", TextType.IMAGE, "https://th-thumbnailer.cdn-si-edu.com/QZfWhcNzUihCbdc3lXSVf5KViXk=/800x600/filters:focal(393x403:394x404)/https://tf-cmsv2-smithsonianmag-media.s3.amazonaws.com/filer/b1/ef/b1ef12c3-d5cd-4c7e-882c-290ffc946a33/greysealpupday2web.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://th-thumbnailer.cdn-si-edu.com/QZfWhcNzUihCbdc3lXSVf5KViXk=/800x600/filters:focal(393x403:394x404)/https://tf-cmsv2-smithsonianmag-media.s3.amazonaws.com/filer/b1/ef/b1ef12c3-d5cd-4c7e-882c-290ffc946a33/greysealpupday2web.jpg", "alt": "This is an image text node" })

    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.NORMAL),
        ])
    def test_split_nodes_delimiter_only_one_instance_of_delimiter(self):
        node = TextNode("This is text with a `code block word", TextType.NORMAL)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            str(context.exception), "Invalid markdown: no closing delimiter")
    def test_split_nodes_delimiter_no_instances_of_delimiter(self):
        node = TextNode("This is text without a code block word", TextType.NORMAL)
        new_node = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_node, [TextNode("This is text without a code block word", TextType.NORMAL)])
    def test_split_nodes_delimiter_four_instances_of_delimiter(self):
        node = TextNode("This is `text` with two `code block` words", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
                TextNode("This is ", TextType.NORMAL),
                TextNode("text", TextType.CODE),
                TextNode(" with two ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" words", TextType.NORMAL)
        ])
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.wikipedia.org/)"
        )
        self.assertListEqual([("link", "https://www.wikipedia.org/")], matches)

if __name__ == "__main__":
    unittest.main()

