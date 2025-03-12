from textnode import TextNode, TextType

def main():
	test_node = TextNode("this is a test node", TextType.LINK, "https://www.google.com/") 

	print(test_node)
	


main()
