import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
  new_nodes = []
  for node in old_nodes:
    if node.text_type != TextType.NORMAL:
      new_nodes.append(node)
      continue
    
    count_delimiter = node.text.count(delimiter)
        
    if count_delimiter % 2 == 1:
      raise Exception(f"Invalid MD: Matching closing delimiter({delimiter}) not found ")
    
    node_text = node.text.split(delimiter)
    for i in range(len(node_text)):
      if not node_text[i].strip():
        continue
      if i % 2 == 1:
        new_nodes.append(TextNode(node_text[i], text_type))
        continue
        
      new_nodes.append(TextNode(node_text[i], TextType.NORMAL))
      
  return new_nodes

def extract_markdown_links(text):
  matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
  return matches

def extract_markdown_images(text):
  matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
  return matches