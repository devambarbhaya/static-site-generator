import unittest
from text_node import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_links, extract_markdown_images

class TestInlineMarkdown(unittest.TestCase):
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
    
  def test_single_link(self):
    text = "Check out [Google](https://google.com)"
    result = extract_markdown_links(text)
    expected = [("Google", "https://google.com")]
    self.assertEqual(result, expected)

  def test_multiple_links(self):
    text = "Here is [Google](https://google.com) and [OpenAI](https://openai.com)"
    result = extract_markdown_links(text)
    expected = [("Google", "https://google.com"), ("OpenAI", "https://openai.com")]
    self.assertEqual(result, expected)

  def test_no_links(self):
    text = "This is plain text with no links."
    result = extract_markdown_links(text)
    expected = []
    self.assertEqual(result, expected)

  def test_empty_text(self):
    text = ""
    result = extract_markdown_links(text)
    expected = []
    self.assertEqual(result, expected)

  def test_link_without_parentheses(self):
    text = "Check out [Google]."
    result = extract_markdown_links(text)
    expected = []
    self.assertEqual(result, expected)

  def test_link_without_brackets(self):
    text = "(https://google.com)"
    result = extract_markdown_links(text)
    expected = []
    self.assertEqual(result, expected)

  def test_nested_brackets(self):
    text = "Check out [[Google]](https://google.com)"
    result = extract_markdown_links(text)
    expected = [("[Google]", "https://google.com")]
    self.assertEqual(result, expected)

  def test_malformed_link(self):
    text = "Check out [Google(https://google.com)"
    result = extract_markdown_links(text)
    expected = []
    self.assertEqual(result, expected)

  def test_text_with_special_characters(self):
    text = "Check out [Goo*gle](https://google.com)"
    result = extract_markdown_links(text)
    expected = [("Goo*gle", "https://google.com")]
    self.assertEqual(result, expected)

  def test_url_with_special_characters(self):
    text = "Check out [Google](https://google.com/search?q=test&lang=en)"
    result = extract_markdown_links(text)
    expected = [("Google", "https://google.com/search?q=test&lang=en")]
    self.assertEqual(result, expected)
    
  def test_single_valid_image(self):
    self.assertEqual(
      extract_markdown_images('![Alt text](https://example.com/image.png)'),
      [('Alt text', 'https://example.com/image.png')]
    )

  def test_multiple_valid_images(self):
    self.assertEqual(
      extract_markdown_images('![Image1](https://example.com/1.png) ![Image2](https://example.com/2.png)'),
      [('Image1', 'https://example.com/1.png'), ('Image2', 'https://example.com/2.png')]
    )

  def test_no_images(self):
    self.assertEqual(extract_markdown_images('No images here!'), [])

  def test_empty_string(self):
    self.assertEqual(extract_markdown_images(''), [])

  def test_image_without_parentheses(self):
    self.assertEqual(extract_markdown_images('![Alt text]https://example.com/image.png'), [])

  def test_image_without_brackets(self):
    self.assertEqual(extract_markdown_images('![](https://example.com/image.png)'), [('', 'https://example.com/image.png')])

  def test_nested_brackets(self):
    self.assertEqual(
      extract_markdown_images('![Alt [nested] text](https://example.com/image.png)'),
      [('Alt [nested] text', 'https://example.com/image.png')]
    )

  def test_malformed_image_syntax(self):
    self.assertEqual(extract_markdown_images('![Alt text (https://example.com/image.png)'), [])

  def test_special_characters_in_alt_text(self):
    self.assertEqual(
      extract_markdown_images('![Alt @#&$% text](https://example.com/image.png)'),
      [('Alt @#&$% text', 'https://example.com/image.png')]
    )

  def test_special_characters_in_url(self):
    self.assertEqual(
      extract_markdown_images('![Alt text](https://example.com/image-@#&$%.png)'),
      [('Alt text', 'https://example.com/image-@#&$%.png')]
    )
    
if __name__ == "__main__":
  unittest.main()