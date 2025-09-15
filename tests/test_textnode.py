import unittest
from src.textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq_same(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_eq_different_text(self):
        node1 = TextNode("Hello", TextType.TEXT)
        node2 = TextNode("World", TextType.TEXT)
        self.assertNotEqual(node1, node2)

    def test_eq_different_type(self):
        node1 = TextNode("Same text", TextType.TEXT)
        node2 = TextNode("Same text", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_eq_different_url(self):
        node1 = TextNode("Click me", TextType.LINK, url="https://example.com")
        node2 = TextNode("Click me", TextType.LINK, url="https://other.com")
        self.assertNotEqual(node1, node2)

    def test_eq_with_non_textnode(self):
        node = TextNode("Hello", TextType.TEXT)
        self.assertNotEqual(node, "Hello")  # should not be equal to a string

    def test_repr(self):
        node = TextNode("Hello", TextType.BOLD, url="https://example.com")
        expected = "TextNode('Hello', TextType.BOLD, 'https://example.com')"
        self.assertEqual(repr(node), expected)


if __name__ == "__main__":
    unittest.main()
