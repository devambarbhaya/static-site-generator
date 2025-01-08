import unittest
from extractmarkdownimages import extract_markdown_images

class TestExtractMarkdownImages(unittest.TestCase):
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