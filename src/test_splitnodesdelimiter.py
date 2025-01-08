import unittest
from textnode import TextNode, TextType
from splitnodesdelimiter import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
  def test_correct_split_normal_and_special(self):
    nodes = [TextNode("Hello **world**!", TextType.NORMAL)]
    result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    expected = [
      TextNode("Hello ", TextType.NORMAL),
      TextNode("world", TextType.BOLD),
      TextNode("!", TextType.NORMAL)
    ]
    self.assertEqual(result, expected)
    
  def test_skip_empty_strings(self):
    nodes = [TextNode("Hello **world****!**", TextType.NORMAL)]
    result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    expected = [
      TextNode("Hello ", TextType.NORMAL),
      TextNode("world", TextType.BOLD),
      TextNode("!", TextType.BOLD),
    ]
    self.assertEqual(result, expected)
    
  def test_preserve_non_normal_nodes(self):
    nodes = [TextNode("This is a title", TextType.BOLD)]
    result = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    # Should remain unchanged since it is a non-normal node
    self.assertEqual(result, nodes)
    
  def test_handle_text_without_delimiter(self):
    nodes = [TextNode("Just a simple sentence.", TextType.NORMAL)]
    result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    # Should remain unchanged as there is no delimiter
    self.assertEqual(result, nodes)
    
  def test_unbalanced_delimiters(self):
    nodes = [TextNode("Unbalanced **text here", TextType.NORMAL)]
    with self.assertRaises(Exception) as context: split_nodes_delimiter(nodes, "**", TextType.BOLD)
    self.assertEqual(str(context.exception), "Invalid MD: Matching closing delimiter(**) not found ")

  def test_multiple_delimiters(self):
    nodes = [TextNode("This **is** bold and *italic* together", TextType.NORMAL)]
    result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    result = split_nodes_delimiter(result, "*", TextType.ITALIC)
    expected = [
      TextNode("This ", TextType.NORMAL),
      TextNode("is", TextType.BOLD),
      TextNode(" bold and ", TextType.NORMAL),
      TextNode("italic", TextType.ITALIC),
      TextNode(" together", TextType.NORMAL)
    ]
    self.assertEqual(result, expected)