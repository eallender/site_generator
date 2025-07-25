import os
import shutil

from utils.convert import markdown_to_html_node
from utils.regex import extract_title

def clear_directory(path: str) -> bool:
    """Clears all files and directories in a destination directory

    Args:
        path (str): The destination directory to be cleared

    Returns:
        bool: True if successful clear
    """
    if not os.path.exists(path):
        return False
    
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            shutil.rmtree(os.path.join(root, name))
    return True

def copy_files_to_dir(source: str, destination: str) -> bool:
    """Copies all files and directory in source to destination

    Args:
        source (str): The source directory to copy files from
        destination (str): The destination directory to copy files to

    Returns:
        bool: True if successful copy
    """
    if not os.path.exists(source):
        return False
    
    shutil.copytree(source, destination, dirs_exist_ok=True)
    return True

def generate_public() -> bool:
    """Clears the current public directory and copies static to public

    Returns:
        bool: True if public generation successful
    """
    main_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(os.path.dirname(main_dir))
    public_path = os.path.join(project_dir, "public")
    static_path = os.path.join(project_dir, "static")

    return clear_directory(public_path) and copy_files_to_dir(static_path, public_path)

def generate_page(from_path: str, template_path: str, dest_path: str):
    """Generates the HTML page for the website

    Args:
        from_path (str): The markdown file path to be rendered on the webpage
        template_path (str): The template html file path
        dest_path (str): The path to the html file
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown_contents = f.read()

    with open(template_path, "r") as f:
        template_contents = f.read()

    html = markdown_to_html_node(markdown_contents)
    title = extract_title(markdown_contents)

    template_contents = template_contents.replace("{{ Title }}", title)
    content = template_contents.replace("{{ Content }}", html.to_html())

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(content)