from enum import Enum
from htmlnode import LeafNode
class TextType(Enum):
  NORMAL = "normal"
  BOLD = "bold"
  ITALIC = "italic"
  CODE = "code"
  LINKS = "links"
  IMAGES = "images"
  
class TextNode:
  def __init__(self, text, text_type: TextType, url=None):
    self.text = text
    self.text_type = text_type
    self.url = url
    
  def __eq__(self, other):
    if self.text == other.text:
      if self.text_type == other.text_type:
        if self.url == other.url:
          return True
        
    return False
  
  def __repr__(self):
    return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
        
def text_node_to_html_node(text_node):
  match text_node.text_type:
    case TextType.NORMAL:
      return LeafNode(value=text_node.text)
    case TextType.BOLD:
      return LeafNode(tag="b", value=text_node.text)
    case TextType.ITALIC:
      return LeafNode(tag="i", value=text_node.text)
    case TextType.CODE:
      return LeafNode(tag="code", value=text_node.text)
    case TextType.LINKS:
      if not text_node.url:
        raise ValueError("URL must be provided for link type.")
      return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    case TextType.IMAGES:
      if not text_node.url:
        raise ValueError("URL must be provided for image type.")
      return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
    case _:
      raise ValueError(f"Unknown TextType: {text_node.text_type}")