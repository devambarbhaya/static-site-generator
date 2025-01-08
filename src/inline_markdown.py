import re
from text_node import TextNode, TextType

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

def split_nodes_images(old_nodes):
  new_nodes = []
  for node in old_nodes:
    if node.text_type != TextType.NORMAL:
      new_nodes.append(node)
      continue
  
    matches = extract_markdown_images(node.text)
    if not matches:
      new_nodes.append(node)
      continue
    
    remaining_text = node.text
    for alt_text, image_url in matches:
      sections = remaining_text.split(f"![{alt_text}]({image_url})", 1)
      if sections[0]:
        new_nodes.append(TextNode(sections[0], TextType.NORMAL))
      new_nodes.append(TextNode(alt_text, TextType.IMAGES, image_url))
      remaining_text = sections[1] if len(sections) > 1 else ""
      
    if remaining_text:
      new_nodes.append(TextNode(remaining_text, TextType.NORMAL))
      
  return new_nodes
    
    
def split_nodes_link(old_nodes):
  new_nodes = []
  for node in old_nodes:
      if node.text_type != TextType.NORMAL:
          new_nodes.append(node)
          continue

      matches = extract_markdown_links(node.text)
      if not matches:
          new_nodes.append(node)
          continue

      remaining_text = node.text
      for link_text, link_url in matches:
          sections = remaining_text.split(f"[{link_text}]({link_url})", 1)
          if sections[0]:
              new_nodes.append(TextNode(sections[0], TextType.NORMAL))
          new_nodes.append(TextNode(link_text, TextType.LINKS, link_url))
          remaining_text = sections[1] if len(sections) > 1 else ""

      if remaining_text:
          new_nodes.append(TextNode(remaining_text, TextType.NORMAL))

  return new_nodes

def text_to_text_node(text):
  nodes = [TextNode(text, TextType.NORMAL)]
  
  nodes = split_nodes_images(nodes)
  nodes = split_nodes_link(nodes)
  nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
  nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
  nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
  
  return nodes