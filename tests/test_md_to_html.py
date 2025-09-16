import unittest
from src.md_to_html import markdown_to_html_node

class TestMarkdownToHTML(unittest.TestCase):

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = (
            "<div>"
            "<p>This is <b>bolded</b> paragraph text in a p tag here</p>"
            "<p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p>"
            "</div>"
        )
        self.assertEqual(html, expected)

    def test_codeblock(self):
        md = "```line 1 of code\nline 2 of code```"
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = (
            "<div>"
            "<pre><code>line 1 of code\nline 2 of code</code></pre>"
            "</div>"
        )
        self.assertEqual(html, expected)
    
    def test_headings(self):
        md = "# Heading 1\n\n## Heading 2\n\n### Heading 3"
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = (
            "<div>"
            "<h1>Heading 1</h1>"
            "<h2>Heading 2</h2>"
            "<h3>Heading 3</h3>"
            "</div>"
        )
        self.assertEqual(html, expected)
    
    def test_quotes(self):
        md = "> Quote line 1\n> Quote line 2"
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = (
            "<div>"
            "<blockquote>Quote line 1\nQuote line 2</blockquote>"
            "</div>"
        )
        self.assertEqual(html, expected)
    
    def test_unordered_list(self):
        md = "- item 1\n- item 2\n- item 3"
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = (
            "<div>"
            "<ul>"
            "<li>item 1</li>"
            "<li>item 2</li>"
            "<li>item 3</li>"
            "</ul>"
            "</div>"
        )
        self.assertEqual(html, expected)
    
    def test_ordered_list(self):
        md = "1. first\n2. second\n3. third"
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = (
            "<div>"
            "<ol>"
            "<li>first</li>"
            "<li>second</li>"
            "<li>third</li>"
            "</ol>"
            "</div>"
        )
        self.assertEqual(html, expected)

if __name__ == "__main__":
    unittest.main()