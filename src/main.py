from textnode import TextNode, TextType
from htmlnode import HTMLNode

def main():
  textnode_trial = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
  print(textnode_trial.__repr__())
  
  htmlnode_trial = HTMLNode("p", "paragraph", [], {})
  print(htmlnode_trial.__repr__())
  
main()