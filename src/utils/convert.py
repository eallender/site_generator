from enum import Enum
from htmlnode import LeafNode
from textnode import TextNode, TextType
from utils.regex import extract_markdown_links, extract_markdown_images, is_block_heading, is_block_code

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

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


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type not in TextType:
            new_nodes.append(node)
            continue

        matches = extract_markdown_images(node.text)

        new_nodes = old_nodes.copy()
        for match in matches:
            delim = f"![{match[0]}]({match[1]})"
            working_list = []
            for curr_node in new_nodes:
                hasRun = False
                while len(curr_node.text.split(delim, maxsplit=1)) > 1:
                    hasRun = True
                    split_node = curr_node.text.split(delim, maxsplit=1)
                    curr_node.text = split_node[1]
                    if split_node[0]:
                        new_node = TextNode(split_node[0], node.text_type)
                        working_list.append(new_node)
                    new_node = TextNode(match[0], TextType.IMAGE, match[1])
                    working_list.append(new_node)
                if curr_node.text:
                    if hasRun:
                        new_node = TextNode(curr_node.text, node.text_type)
                        working_list.append(new_node)
                    else:
                        working_list.append(curr_node)
            new_nodes = working_list

    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type not in TextType:
            new_nodes.append(node)
            continue

        matches = extract_markdown_links(node.text)

        new_nodes = old_nodes.copy()
        for match in matches:
            delim = f"[{match[0]}]({match[1]})"
            working_list = []
            for curr_node in new_nodes:
                hasRun = False
                while len(curr_node.text.split(delim, maxsplit=1)) > 1:
                    hasRun = True
                    split_node = curr_node.text.split(delim, maxsplit=1)
                    curr_node.text = split_node[1]
                    if split_node[0]:
                        new_node = TextNode(split_node[0], node.text_type)
                        working_list.append(new_node)
                    new_node = TextNode(match[0], TextType.LINK, match[1])
                    working_list.append(new_node)
                if curr_node.text:
                    if hasRun:
                        new_node = TextNode(curr_node.text, node.text_type)
                        working_list.append(new_node)
                    else:
                        working_list.append(curr_node)
            new_nodes = working_list

    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    text_delims = ["**", "_", "`"]
    text_types = [TextType.BOLD, TextType.ITALIC, TextType.CODE]

    for delim,type in zip(text_delims, text_types):
        nodes = split_nodes_delimiter(nodes, delim, type)

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes

def markdown_to_blocks(markdown: str):
    blocks = []
    splits = markdown.split("\n\n")

    for split in splits:
        split = split.strip()
        if not split:
            continue
        
        blocks.append(split)

    return blocks

def is_block_quote(block: str) -> bool:
    lines = block.splitlines()

    for line in lines:
        if not line.startswith(">"):
            return False
    return True

def is_block_unordered_list(block: str) -> bool:
    lines = block.splitlines()

    for line in lines:
        if not line.startswith("- "):
            return False
    return True

def is_block_ordered_list(block: str) -> bool:
    lines = block.splitlines()

    list_num = 1
    for line in lines:
        if not line.startswith(f"{list_num}. "):
            return False
        list_num += 1
    return True

def block_to_block_type(block: str):
    if is_block_heading(block):
        return BlockType.HEADING
    if is_block_code(block):
        return BlockType.CODE
    if is_block_quote(block):
        return BlockType.QUOTE
    if is_block_unordered_list(block):
        return BlockType.UNORDERED_LIST
    if is_block_ordered_list(block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
        