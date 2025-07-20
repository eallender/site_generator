from htmlnode import LeafNode
from textnode import TextNode, TextType

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type not in TextType:
        raise Exception(f"Invalid text type received: {text_node.text_type}")
    
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, props={"href": text_node.url})
        case TextType.IMAGE: 
            return LeafNode("img", "", props={"src": text_node.url, "alt": text_node.text})
        
def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type not in TextType:
            new_nodes.append(node)
            continue

        in_delim = False
        while len(node.text.split(delimiter, maxsplit=1)) > 1:
            split_node = node.text.split(delimiter, maxsplit=1)
            node.text = split_node[1]
            if in_delim:
                new_node = TextNode(split_node[0], text_type)
                in_delim = False
            else:
                in_delim = True
                if not split_node[0]:
                    continue
                new_node = TextNode(split_node[0], node.text_type)
            new_nodes.append(new_node)
            
        if in_delim:
            raise Exception(f"Invalid syntax, missing matching '{delimiter}' in {node}")
        else:
            if node.text:
                new_node = TextNode(node.text, node.text_type)
                new_nodes.append(new_node)

    return new_nodes