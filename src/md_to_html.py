from .htmlnode import LeafNode, ParentNode
from .md_inline import text_to_text_nodes
from .md_block import markdown_to_blocks, block_to_block_type, BlockType
from .textnode import text_node_to_html_node, TextNode, TextType


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    html_children = []
    
    for block in blocks:
        block_type = block_to_block_type(block)
        
        match block_type:
            case BlockType.PARAGRAPH:
                html_children.append(paragraph_to_html(block))
                
            case BlockType.HEADING:
                html_children.append(heading_to_html(block))    
                
            case BlockType.CODE:
                html_children.append(code_to_html(block))
                
            case BlockType.QUOTE:
                html_children.append(quote_to_html(block))
                
            case BlockType.UNORDERED_LIST:
                html_children.append(ul_to_html(block))
                
            case BlockType.ORDERED_LIST:
                html_children.append(ol_to_html(block))
                
    return ParentNode("div", html_children)


def text_to_children(text: str) -> list[LeafNode]:
    text_nodes = text_to_text_nodes(text)
    html_children = [text_node_to_html_node(node) for node in text_nodes]
    
    return html_children


def paragraph_to_html(block: str) -> ParentNode:
    text = " ".join(line.strip() for line in block.splitlines())
    children = text_to_children(text)
    
    return ParentNode("p", children)
    

def heading_to_html(block: str) -> ParentNode:
    prefix, text = block.split(" ", 1)
    tag = f"h{len(prefix)}"
    children = text_to_children(text)
    
    return ParentNode(tag, children)
    

def code_to_html(block: str) -> ParentNode:
    code_text = block.strip("`")
    code_node = text_node_to_html_node(TextNode(code_text, TextType.CODE))
    return ParentNode("pre", [code_node])

    
def quote_to_html(block: str) -> ParentNode:
    lines = [line.lstrip("> ").rstrip() for line in block.splitlines()]
    text = "\n".join(lines)
    children = text_to_children(text)

    return ParentNode("blockquote", children)

    
def ul_to_html(block: str) -> ParentNode:
    lines = [line.lstrip("- ").rstrip() for line in block.splitlines()]
    li_nodes = [ParentNode("li", text_to_children(line)) for line in lines]
        
    return ParentNode("ul", li_nodes)
    
    
def ol_to_html(block: str) -> ParentNode:
    lines = block.splitlines()
    li_nodes = []

    for i, line in enumerate(lines):
        prefix = f"{i+1}. "
        content = line.removeprefix(prefix).rstrip()
        li_nodes.append(ParentNode("li", text_to_children(content)))

    return ParentNode("ol", li_nodes)