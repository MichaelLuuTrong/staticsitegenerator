from enum import Enum

import re

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
		return (f"TextNode({self.text}, {(self.text_type).name}, {self.url})")
	
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

def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    images = re.findall(pattern, text)
    return images

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    links = re.findall(pattern, text)
    return links

def split_nodes_image(old_nodes):
	res = []
	# operate on each node individually
	for node in old_nodes:
		if node.text_type != TextType.NORMAL:
				res.append(node)
				continue
	
		split_node_text_array = []
		found_image_text_array = extract_markdown_images(node.text)
		node_text = node.text

		for found_image_text in found_image_text_array:
			reconstructed_image_text = f"![{found_image_text[0]}]({found_image_text[1]})"
			index_of_image_start = node_text.find(reconstructed_image_text)
			index_of_image_end = index_of_image_start + len(reconstructed_image_text)

			before_image = node_text[:index_of_image_start]
			if before_image:  # Only create a node if there's actual text before the image
				before_image_textnode = TextNode(before_image, TextType.NORMAL)
				split_node_text_array.append(before_image_textnode)
			
			image_textnode = TextNode(found_image_text[0], TextType.IMAGE, found_image_text[1])
			split_node_text_array.append(image_textnode)

			# remove the node_text that has already been accounted for
			node_text = node_text[index_of_image_end:]

		if node_text:
			remaining_textnode = TextNode(node_text, TextType.NORMAL)
			split_node_text_array.append(remaining_textnode)

		res.extend(split_node_text_array)

	return res

def split_nodes_link(old_nodes):
    res = []
    # operate on each node individually
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            res.append(node)
            continue
        
        split_node_text_array = []
        found_link_text_array = extract_markdown_links(node.text)
        node_text = node.text

        for found_link_text in found_link_text_array:
            reconstructed_link_text = f"[{found_link_text[0]}]({found_link_text[1]})"
            index_of_link_start = node_text.find(reconstructed_link_text)
            index_of_link_end = index_of_link_start + len(reconstructed_link_text)

            before_link = node_text[:index_of_link_start]
            if before_link:  # Only create a node if there's actual text before the link
                before_link_textnode = TextNode(before_link, TextType.NORMAL)
                split_node_text_array.append(before_link_textnode)
            
            link_textnode = TextNode(found_link_text[0], TextType.LINK, found_link_text[1])
            split_node_text_array.append(link_textnode)

            # remove the node_text that has already been accounted for
            node_text = node_text[index_of_link_end:]

        if node_text:
            remaining_textnode = TextNode(node_text, TextType.NORMAL)
            split_node_text_array.append(remaining_textnode)

        res.extend(split_node_text_array)

    return res

def text_to_textnodes(text):
	nodes = [TextNode(text, TextType.NORMAL)]
	nodes = split_nodes_image(nodes)
	nodes = split_nodes_link(nodes)
	nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
	nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
	nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
	return nodes

