import re

def extract_markdown_images(text: str) -> list[str]:
    """Finds all markdown images within the given text

    Args:
        text (str): The text to be checked for images

    Returns:
        list[str]: The markdown images in the text
    """
    reg = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(reg, text)

def extract_markdown_links(text: str) -> list[str]:
    """Finds all markdown links within the given text

    Args:
        text (str): The test to be checked for links

    Returns:
        list[str]: The markdown links in the text
    """
    reg = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(reg, text)

def is_block_heading(block: str) -> bool:
    """Checks to see if a given markdown block is a heading

    Args:
        block (str): The markdown block to be checked

    Returns:
        bool: True if it is a heading block
    """
    reg = r"^#{1,6} [^\n]"
    match = re.match(reg, block)
    if match:
        return True
    return False

def is_block_code(block: str) -> bool:
    """Checks to see if a given markdown block is a code block

    Args:
        block (str): The markdown block to be checked

    Returns:
        bool: True if it is a code block
    """
    reg = r"```(.*?)```"
    match = re.fullmatch(reg, block, re.DOTALL)
    if match:
            return True
    return False

def get_heading(block: str) -> str | None:
    """Gets the heading from a markdown heading block

    Args:
        block (str): The block containing the heading

    Returns:
        str | None: The heading format text found with the string (ex: "##### Heading 5" --> "##### ")
    """
    match = re.match(r"^(#{1,6}\s)", block)
    if match:
        return match.group(1)
    return None

def remove_ordered_list_prefix(line: str) -> str:
    """Gets the list number from a line in an ordered list

    Args:
        line (str): A line of an ordered list

    Returns:
        str: The line with the list number removed (ex: "1. item 1" --> "item 1")
    """
    return re.sub(r"^\d+\.\s+", "", line)

def extract_title(markdown: str) -> str:
    """Extracts the title from a markdown file (# Title)

    Args:
        markdown (str): The markdown text document

    Raises:
        Exception: Markdown file missing header

    Returns:
        str: Markdown title
    """
    for line in markdown.splitlines():
        line = line.strip()
        match = re.match(r"^# (.+)", line)
        if match:
            return match.group(1)
        
    raise Exception("Markdown file is missing header!")


