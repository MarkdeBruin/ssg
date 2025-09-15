import unittest
from src.htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_init_defaults(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})

    def test_props_to_html_empty(self):
        node = HTMLNode(tag="p")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single(self):
        node = HTMLNode(tag="a", props={"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')

    def test_props_to_html_multiple(self):
        node = HTMLNode(tag="a", props={"href": "https://example.com", "target": "_blank"})
        result = node.props_to_html()
        # dicts may not preserve order in older Python versions
        self.assertTrue(result == ' href="https://example.com" target="_blank"' or
                        result == ' target="_blank" href="https://example.com"')

    def test_repr(self):
        node = HTMLNode(tag="p", value="Hello", props={"class": "intro"})
        expected = "HTMLNode(tag='p', value='Hello', children=[], props={'class': 'intro'})"
        self.assertEqual(repr(node), expected)

    def test_children_assignment(self):
        child = HTMLNode(tag="span", value="child")
        parent = HTMLNode(tag="div", children=[child])
        self.assertEqual(parent.children[0], child)
        self.assertEqual(parent.children[0].tag, "span")
        self.assertEqual(parent.children[0].value, "child")


if __name__ == "__main__":
    unittest.main()
