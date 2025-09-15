from .textnode import TextNode, TextType
from .htmlnode import LeafNode
from .nodes_parser import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)

def text_to_text_nodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes


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
