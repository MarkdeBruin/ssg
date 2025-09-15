import unittest
from src.textnode import TextNode, TextType
from src.nodes_parser import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):

    def test_basic_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " text")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_starts_with_delimiter(self):
        node = TextNode("**bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result[0].text_type, TextType.BOLD)
        self.assertEqual(result[1].text_type, TextType.TEXT)

    def test_ends_with_delimiter(self):
        node = TextNode("Text **bold**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result[-1].text_type, TextType.BOLD if len(result) == 2 else TextType.TEXT)

    def test_multiple_occurrences(self):
        node = TextNode("**b1** middle **b2** end", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result[0].text, "b1")
        self.assertEqual(result[1].text, " middle ")
        self.assertEqual(result[2].text, "b2")
        self.assertEqual(result[3].text, " end")

    def test_consecutive_delimiters(self):
        node = TextNode("Text **** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        # empty string between delimiters should be skipped
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "Text ")
        self.assertEqual(result[1].text, " text")

    def test_different_delimiters(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(result[1].text_type, TextType.ITALIC)
        self.assertEqual(result[1].text, "italic")

    def test_code_delimiter(self):
        node = TextNode("Here is `code` example", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[1].text, "code")

    def test_non_text_nodes_preserved(self):
        node1 = TextNode("plain", TextType.TEXT)
        node2 = TextNode("bold", TextType.BOLD)
        result = split_nodes_delimiter([node1, node2], "**", TextType.BOLD)
        self.assertEqual(result[1].text_type, TextType.BOLD)  # original bold node preserved

if __name__ == "__main__":
    unittest.main()
