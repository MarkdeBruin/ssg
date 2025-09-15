import unittest
from src.textnode import TextNode, TextType
from src.htmlnode import LeafNode
from src.converters import text_to_text_nodes, text_node_to_html_node

class TestTextToTextNodes(unittest.TestCase):

    def test_text_to_text_nodes_complex(self):
        text = (
            "This is **bold** with _italic_ and `code` "
            "and an ![image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )
        nodes = text_to_text_nodes(text)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" with ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        self.assertEqual(len(nodes), len(expected))
        for node, exp in zip(nodes, expected):
            self.assertEqual(node.text, exp.text)
            self.assertEqual(node.text_type, exp.text_type)
            self.assertEqual(getattr(node, "url", None), getattr(exp, "url", None))

    def test_text_to_text_nodes_only_text(self):
        text = "Just plain text here."
        nodes = text_to_text_nodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, text)
        self.assertEqual(nodes[0].text_type, TextType.TEXT)

    def test_text_to_text_nodes_multiple_images_and_links(self):
        text = (
            "![img1](url1) then [link1](link1_url) "
            "and ![img2](url2) with [link2](link2_url)"
        )
        nodes = text_to_text_nodes(text)

        expected = [
            TextNode("img1", TextType.IMAGE, "url1"),
            TextNode(" then ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "link1_url"),
            TextNode(" and ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "url2"),
            TextNode(" with ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "link2_url"),
        ]

        self.assertEqual(len(nodes), len(expected))
        for node, exp in zip(nodes, expected):
            self.assertEqual(node.text, exp.text)
            self.assertEqual(node.text_type, exp.text_type)
            self.assertEqual(getattr(node, "url", None), getattr(exp, "url", None))


class TestTextNodeToHTMLNode(unittest.TestCase):

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")

    def test_code(self):
        node = TextNode("print('Hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('Hello')")

    def test_link(self):
        node = TextNode("Click me", TextType.LINK, url="https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image(self):
        node = TextNode("Alt text", TextType.IMAGE, url="https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://example.com/image.png", "alt": "Alt text"})

    def test_link_missing_url_raises(self):
        node = TextNode("Click me", TextType.LINK)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_image_missing_url_raises(self):
        node = TextNode("Alt text", TextType.IMAGE)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_unknown_type_raises(self):
        class FakeType:
            pass
        node = TextNode("Oops", FakeType())
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)


if __name__ == "__main__":
    unittest.main()
