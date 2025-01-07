from textnode import TextNode, TextType

def main():
  trial = TextNode("This is a text node", TextType.BOLD_TEXT, "https://www.boot.dev")
  print(trial.__repr__())
  
  
main()