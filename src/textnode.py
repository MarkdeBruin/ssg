from .htmlnode import LeafNode
from enum import Enum


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text!r}, {self.text_type}, {self.url!r})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if not isinstance(text_node, TextNode):
        raise TypeError("Expected a TextNode object")

    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)

        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)

        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)

        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)

        case TextType.LINK:
            if not text_node.url:
                raise ValueError("LINK TextNode must have a URL")
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})

        case TextType.IMAGE:
            if not text_node.url:
                raise ValueError("IMAGE TextNode must have a URL")
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})

        case _:
            raise ValueError(f"Unknown TextType: {text_node.text_type}")