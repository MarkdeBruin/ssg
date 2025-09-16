import re
from src.textnode import TextType, TextNode


def text_to_text_nodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes
    

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
            
        split_node = node.text.split(delimiter)
        for i, piece in enumerate(split_node):
            if not piece:
                continue
            if len(split_node) % 2 == 0:
                raise ValueError("invalid markdown, formatted section not closed")
            node_type = text_type if i % 2 == 1 else TextType.TEXT
            new_nodes.append(TextNode(piece, node_type))
    
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = extract_markdown_images(node.text)
        if not matches:
            new_nodes.append(node)
            continue

        new_nodes.extend(split_node_by_matches(node, matches, TextType.IMAGE, markdown_prefix="!"))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = extract_markdown_links(node.text)
        if not matches:
            new_nodes.append(node)
            continue

        new_nodes.extend(split_node_by_matches(node, matches, TextType.LINK))

    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_node_by_matches(node, matches, node_type, markdown_prefix=""):
    new_nodes = []
    text = node.text

    for text_value, url in matches:
        markdown = f"{markdown_prefix}[{text_value}]({url})"
        before, after = text.split(markdown, 1)

        if before:
            new_nodes.append(TextNode(before, TextType.TEXT))

        new_nodes.append(TextNode(text_value, node_type, url=url))
        text = after

    if text:
        new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes