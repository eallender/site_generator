import re

def extract_markdown_images(text):
    reg = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(reg, text)

def extract_markdown_links(text):
    reg = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(reg, text)
