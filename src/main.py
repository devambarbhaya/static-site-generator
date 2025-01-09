import os
import shutil
from text_node import TextNode, TextType
from html_node import HTMLNode

def copy_static(source, destination):
  if os.path.exists(destination):
    shutil.rmtree(destination)
    print(f"Deleted existing destination: {destination}")
    
  os.makedirs(destination)
  print(f"Created directory: {destination}")
  
  for item in os.listdir(source):
    source_item = os.path.join(source, item)
    destination_item = os.path.join(destination, item)
    
    if os.path.isfile(source_item):
      shutil.copy(source_item, destination_item)
      print(f"Copied file: {source_item} -> {destination_item}")
    elif os.path.isdir(source_item):
      shutil.copytree(source_item, destination_item)
      print(f"Copied directory: {source_item} -> {destination_item}")

def main():
  copy_static("static", "public")
  
main()