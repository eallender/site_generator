import os
from utils.site_gen import generate_public, generate_pages_recursive

def main():
    if generate_public():
        print("Successfully generated public")
    else:
        print("Failed to generate public")
    main_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(main_dir)
    markdown_path = os.path.join(project_dir, "content")
    template_path = os.path.join(project_dir, "template.html")
    index_path = os.path.join(project_dir, "public")
    generate_pages_recursive(markdown_path, template_path, index_path)
    
if __name__ == "__main__":
    main()