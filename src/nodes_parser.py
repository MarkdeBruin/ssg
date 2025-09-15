from .textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            split_node = node.text.split(delimiter)
            for i, piece in enumerate(split_node):
                if not piece:
                    continue  # skips the empty string
                node_type = text_type if i % 2 == 1 else TextType.TEXT
                new_nodes.append(TextNode(piece, node_type))
    
    return new_nodes