import unittest
from src.textnode import TextNode, TextType
from src.nodes_parser import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    extract_markdown_images,
    extract_markdown_links,
)


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
        self.assertEqual(result[1].text_type, TextType.BOLD)


class TestMarkdownExtraction(unittest.TestCase):
    def test_extract_images_basic(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("rick roll", "https://i.imgur.com/aKaOqIh.gif")])

    def test_extract_images_multiple(self):
        text = "![img1](url1) and ![img2](url2)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("img1", "url1"), ("img2", "url2")])

    def test_extract_links_basic(self):
        text = "Go to [Boot.dev](https://www.boot.dev)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("Boot.dev", "https://www.boot.dev")])

    def test_extract_links_multiple(self):
        text = "Links: [one](url1), [two](url2)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("one", "url1"), ("two", "url2")])

    def test_extract_images_and_links(self):
        text = "Image ![alt](img_url) and link [text](link_url)"
        img_result = extract_markdown_images(text)
        link_result = extract_markdown_links(text)
        self.assertEqual(img_result, [("alt", "img_url")])
        self.assertEqual(link_result, [("text", "link_url")])

    def test_no_matches(self):
        text = "No markdown here"
        self.assertEqual(extract_markdown_images(text), [])
        self.assertEqual(extract_markdown_links(text), [])


class TestSplitNodesImageLink(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) "
            "and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image",
                    TextType.IMAGE,
                    "https://i.imgur.com/3elNhQu.png",
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "Click [here](https://example.com) or [there](https://example.org)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Click ", TextType.TEXT),
                TextNode("here", TextType.LINK, "https://example.com"),
                TextNode(" or ", TextType.TEXT),
                TextNode("there", TextType.LINK, "https://example.org"),
            ],
            new_nodes,
        )

    def test_no_images_or_links(self):
        node = TextNode("Just plain text", TextType.TEXT)
        self.assertListEqual(split_nodes_image([node]), [node])
        self.assertListEqual(split_nodes_link([node]), [node])


if __name__ == "__main__":
    unittest.main()
