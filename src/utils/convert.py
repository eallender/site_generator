from enum import Enum
from htmlnode import LeafNode, HTMLNode, ParentNode
from textnode import TextNode, TextType
from utils.regex import extract_markdown_links, extract_markdown_images, is_block_heading, is_block_code, get_heading, remove_ordered_list_prefix

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    """Converts a text node object into a LeafNode object

    Args:
        text_node (TextNode): The TextNode to convert

    Raises:
        Exception: Invalid text type received for given TextNode

    Returns:
        LeafNode: The new LeafNode created from the TextNode
    """
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
    """Splits each TextNode based on the delimiter passed to the function

    Args:
        old_nodes (list[TextNode]): The list of TextNodes to be split
        delimiter (str): The delimiter that should be used to split the nodes
        text_type (TextType): The text types that new split nodes should become

    Raises:
        Exception: A text node was missing a matching delimiter

    Returns:
        list[TextNode]: The new list of TextNodes after splitting based on the delimiter
    """
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
    """Splits the TextNodes based on markdown images within the text

    Args:
        old_nodes (list[TextNode]): The list of old nodes that will be checked for images

    Returns:
        list[TextNode]: The resulting list of TextNodes after splitting out the images
    """
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
    """Splits the TextNodes based on markdown links within the text

    Args:
        old_nodes (list[TextNode]): The list of old nodes that will be checked for links

    Returns:
        list[TextNode]: The resulting list of TextNodes after splitting out the links
    """
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
    """Converts raw markdown text to TextNode objects

    Args:
        text (str): The raw markdown text to be converted

    Returns:
        list[TextNode]: The resulting list of TextNodes
    """
    nodes = [TextNode(text, TextType.TEXT)]
    text_delims = ["**", "_", "`"]
    text_types = [TextType.BOLD, TextType.ITALIC, TextType.CODE]

    for delim,type in zip(text_delims, text_types):
        nodes = split_nodes_delimiter(nodes, delim, type)

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes

def markdown_to_blocks(markdown: str) -> list[str]:
    """Converts markdown into corresponding blocks

    Args:
        markdown (str): The raw markdown to be split

    Returns:
        list[str]: The list containing the text for each markdown block
    """
    blocks = []
    splits = markdown.split("\n\n")

    for split in splits:
        split = split.strip()
        if not split:
            continue
        
        blocks.append(split)

    return blocks

def is_block_quote(block: str) -> bool:
    """Checks to see if a given block is a quote block

    Args:
        block (str): The block to be checked

    Returns:
        bool: True if it is a quote block
    """
    lines = block.splitlines()

    for line in lines:
        if not line.startswith(">"):
            return False
    return True

def is_block_unordered_list(block: str) -> bool:
    """Checks to see if a given block is an unordered list

    Args:
        block (str): The block to be checked

    Returns:
        bool: True if it is an unordered list
    """
    lines = block.splitlines()

    for line in lines:
        if not line.startswith("- "):
            return False
    return True

def is_block_ordered_list(block: str) -> bool:
    """Checks to see if a given block is an ordered list

    Args:
        block (str): The block to be checked

    Returns:
        bool: True if it is an ordered list
    """
    lines = block.splitlines()

    list_num = 1
    for line in lines:
        if not line.startswith(f"{list_num}. "):
            return False
        list_num += 1
    return True

def block_to_block_type(block: str) -> BlockType:
    """Gets the block type for the given block

    Args:
        block (str): The block to be checked

    Returns:
        BlockType: The type for the given block
    """
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

def get_text_from_block(block: str, block_type: BlockType) -> str:
    """Gets the raw text from a markdown block (removing the block format text)

    Args:
        block (str): The block containing the text
        block_type (BlockType): The type of the corresponding block

    Raises:
        Exception: An invalid block type was received

    Returns:
        str: The raw text of the given block
    """
    match block_type:
        case BlockType.HEADING:
            heading = get_heading(block)
            return block.replace(heading, "").lstrip("\n")
        case BlockType.CODE:
            return block.replace("```", "").lstrip("\n")
        case BlockType.QUOTE:
            lines = block.splitlines()
            text = []
            for line in lines:
                text.append(line.lstrip("> "))
            return " ".join(text)
        case BlockType.UNORDERED_LIST:
            lines = block.splitlines()
            text = []
            for line in lines:
                text.append(line.lstrip("- "))
            return "\n".join(text)
        case BlockType.ORDERED_LIST:
            lines = block.splitlines()
            text = []
            for line in lines:
                text.append(remove_ordered_list_prefix(line))
            return "\n".join(text)
        case BlockType.PARAGRAPH:
            return block.replace("\n", " ")
        case _:
            raise Exception("Invalid block type received.")

def text_to_children(text: str) -> list[LeafNode]:
    """Gets the LeafNodes (children) for the given text

    Args:
        text (str): The raw text of a block (children of the block)

    Returns:
        list[LeafNode]: The LeafNodes for a block (its children)
    """
    children = []
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        children.append(text_node_to_html_node(node))
    
    return children

def block_to_html_node(block: str, block_type: BlockType) -> ParentNode:
    """Converts a markdown block to an HTMLNode (ParentNode)

    Args:
        block (str): A markdown block
        block_type (BlockType): The corresponding type for the given block

    Raises:
        Exception: An invalid block type was received

    Returns:
        ParentNode: The given block converted to a ParentNode
    """
    match block_type:
        case BlockType.HEADING:
            heading = get_heading(block)
            text = get_text_from_block(block, block_type)
            children = text_to_children(text)
            return ParentNode(f"h{len(heading) - 1}", children)
        case BlockType.CODE:
            text = get_text_from_block(block, block_type)
            code_text_block = TextNode(text, TextType.CODE)
            html_node = text_node_to_html_node(code_text_block)
            return ParentNode("pre", [html_node])
        case BlockType.QUOTE:
            text = get_text_from_block(block, block_type)
            children = text_to_children(text)
            return ParentNode("blockquote", children)
        case BlockType.UNORDERED_LIST:
            text = get_text_from_block(block, block_type)
            children = []
            for line in text.splitlines():
                child = text_to_children(line)
                children.append(ParentNode("li", child))
            return ParentNode("ul", children)
        case BlockType.ORDERED_LIST:
            text = get_text_from_block(block, block_type)
            children = []
            for line in text.splitlines():
                child = text_to_children(line)
                children.append(ParentNode("li", child))
            return ParentNode("ol", children)
        case BlockType.PARAGRAPH:
            text = get_text_from_block(block, block_type)
            children = text_to_children(text)
            return ParentNode("p", children)
        case _:
            raise Exception("Invalid block type received.")
    
    return 

def markdown_to_html_node(markdown: str) -> ParentNode:
    """Converts raw markdown to HTML

    Args:
        markdown (str): The raw markdown to be converted

    Returns:
        ParentNode: The HTML for the given markdown text
    """
    blocks = markdown_to_blocks(markdown)
    
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        html_node_block = block_to_html_node(block, block_type)
        children.append(html_node_block)

    return ParentNode("div", children)
        