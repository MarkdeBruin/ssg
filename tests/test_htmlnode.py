import unittest
from src.htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):

    # --- HTMLNode tests ---
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
        self.assertTrue(
            result == ' href="https://example.com" target="_blank"' or
            result == ' target="_blank" href="https://example.com"'
        )

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

    # --- LeafNode tests ---
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_no_value_raises(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None)

    # --- ParentNode tests ---
    def test_parentnode_simple(self):
        node = ParentNode("div", [LeafNode("p", "Hello")])
        self.assertEqual(node.to_html(), "<div><p>Hello</p></div>")

    def test_parentnode_nested(self):
        node = ParentNode("div", [
            LeafNode("p", "Hello"),
            ParentNode("span", [LeafNode("b", "Bold")])
        ])
        self.assertEqual(node.to_html(), "<div><p>Hello</p><span><b>Bold</b></span></div>")

    def test_parentnode_with_props(self):
        node = ParentNode("div", [LeafNode("p", "Text")], props={"class": "container"})
        self.assertEqual(node.to_html(), '<div class="container"><p>Text</p></div>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")

    def test_parentnode_no_tag_raises(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("p", "Hello")]).to_html()

    def test_parentnode_children_must_be_list(self):
        with self.assertRaises(TypeError):
            ParentNode("div", LeafNode("p", "Hello"))


if __name__ == "__main__":
    unittest.main()

