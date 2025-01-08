import unittest
from text_node import TextNode, TextType, text_node_to_html_node
from html_node import LeafNode


class TestTextNode(unittest.TestCase):
  def test_eq(self):
    node = TextNode("This is a text node", TextType.NORMAL)
    node2 = TextNode("This is a text node", TextType.NORMAL)
    self.assertEqual(node, node2)

  def test_eq_false(self):
    node = TextNode("This is a text node", TextType.NORMAL)
    node2 = TextNode("This is a text node2", TextType.NORMAL)
    self.assertNotEqual(node, node2)

  def test_eq_false2(self):
    node = TextNode("This is a text node", TextType.NORMAL)
    node2 = TextNode("This is a text node2", TextType.NORMAL)
    self.assertNotEqual(node, node2)

  def test_eq_url(self):
    node = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
    node2 = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
    self.assertEqual(node, node2)

  def test_repr(self):
    node = TextNode("This is a text node", TextType.NORMAL, "https://www.boot.dev")
    self.assertEqual("TextNode(This is a text node, normal, https://www.boot.dev)", repr(node))

  def test_text_node_to_html_node_normal(self):
    node = TextNode("Hello World", TextType.NORMAL)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node, LeafNode(value="Hello World"))

  def test_text_node_to_html_node_bold(self):
    node = TextNode("Bold Text", TextType.BOLD)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node, LeafNode(tag="b", value="Bold Text"))

  def test_text_node_to_html_node_italic(self):
    node = TextNode("Italic Text", TextType.ITALIC)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node, LeafNode(tag="i", value="Italic Text"))

  def test_text_node_to_html_node_code(self):
    node = TextNode("Code Snippet", TextType.CODE)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node, LeafNode(tag="code", value="Code Snippet"))

  def test_text_node_to_html_node_links(self):
    node = TextNode("Link Text", TextType.LINKS, "https://example.com")
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node, LeafNode(tag="a", value="Link Text", props={"href": "https://example.com"}))

  def test_text_node_to_html_node_images(self):
    node = TextNode("Image Alt", TextType.IMAGES, "https://example.com/image.png")
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node, LeafNode(tag="img", value="", props={"src": "https://example.com/image.png", "alt": "Image Alt"}))

  def test_text_node_to_html_node_link_no_url(self):
    node = TextNode("Link without URL", TextType.LINKS)
    with self.assertRaises(ValueError):
        text_node_to_html_node(node)

  def test_text_node_to_html_node_image_no_url(self):
    node = TextNode("Image without URL", TextType.IMAGES)
    with self.assertRaises(ValueError):
        text_node_to_html_node(node)

  def test_text_node_to_html_node_invalid_type(self):
    node = TextNode("Invalid", None)
    with self.assertRaises(ValueError):
        text_node_to_html_node(node)


if __name__ == "__main__":
    unittest.main()
