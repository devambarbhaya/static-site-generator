import unittest
from extractmarkdownlinks import extract_markdown_links

class TestExtractMarkdownLinks(unittest.TestCase):
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

if __name__ == "__main__":
    unittest.main()
