import re

def extract_markdown_images(text):
    reg = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(reg, text)

def extract_markdown_links(text):
    reg = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(reg, text)

def is_block_heading(block: str) -> bool:
    reg = r"^#{1,6} [^\n]"
    match = re.match(reg, block)
    if match:
        return True
    return False

def is_block_code(block: str) -> bool:
    reg = r"```(.*?)```"
    match = re.fullmatch(reg, block, re.DOTALL)
    if match:
            return True
    return False

def get_heading(block: str) -> str | None:
    match = re.match(r"^(#{1,6}\s)", block)
    if match:
        return match.group(1)
    return None

def remove_ordered_list_prefix(line: str) -> str:
    return re.sub(r"^\d+\.\s+", "", line)



