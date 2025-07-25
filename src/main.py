import os
import sys
from utils.site_gen import generate_public, generate_pages_recursive

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    if generate_public():
        print("Successfully generated public")
    else:
        print("Failed to generate public")
    main_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(main_dir)
    markdown_path = os.path.join(project_dir, "content")
    template_path = os.path.join(project_dir, "template.html")
    index_path = os.path.join(project_dir, "docs")
    generate_pages_recursive(markdown_path, template_path, index_path, basepath)
    
if __name__ == "__main__":
    main()