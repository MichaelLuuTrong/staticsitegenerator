from enum import Enum

from htmlnode import HTMLNode, LeafNode, ParentNode

class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "url"


class TextNode:
	def __init__(self, text, text_type, url = None):
		self.text = text
		self.text_type = text_type
		self.url = url
	def __eq__(self, other_textnode):
		if self.text == other_textnode.text and self.text_type == other_textnode.text_type and self.url == other_textnode.url:
			return True
		else:
			return False
	def __repr__(self):
		return (f"TextNode({self.text}, {(self.text_type).value}, {self.url})")
	
def text_node_to_html_node(text_node):
	match text_node.text_type:
		case TextType.NORMAL:
			return LeafNode(None, text_node.text)
		case TextType.BOLD:
			return LeafNode("b", text_node.text)
		case TextType.ITALIC:
			return LeafNode("i", text_node.text)
		case TextType.CODE:
			return LeafNode("code", text_node.text)
		case TextType.LINK:
			return LeafNode("a", text_node.text, {"href": text_node.url})
		case TextType.IMAGE:
			return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
		case _:
			raise Exception("Invalid text type")
			

def split_nodes_delimiter(old_nodes, delimiter, text_type):
	#old nodes is a list of what appears to be TextNodes
	#returns a new list of nodes, where "text" type nodes in the input are split into multiple nodes
	new_nodes = []
	for node in old_nodes:
		if node.text_type != TextType.NORMAL:
			new_nodes.append(node)
			continue
		text = node.text

		start_idx = text.find(delimiter)
		if start_idx == -1:
			new_nodes.append(node)
			continue
		
		end_idx = text.find(delimiter, start_idx + len(delimiter))
		if end_idx == -1:
			raise Exception("Invalid markdown: no closing delimiter")

		before_text = text[:start_idx]
		between_text = text[start_idx + len(delimiter):end_idx]
		after_text = text[end_idx + len(delimiter):]

		if before_text:
			new_nodes.append(TextNode(before_text, TextType.NORMAL))
		new_nodes.append(TextNode(between_text, text_type))

		if after_text:
			remaining_node = TextNode(after_text, TextType.NORMAL)
			result_nodes = split_nodes_delimiter([remaining_node], delimiter, text_type)
			new_nodes.extend(result_nodes)

	return new_nodes


		



