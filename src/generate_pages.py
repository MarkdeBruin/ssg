import os
from src.md_to_html import markdown_to_html_node
from src.md_meta import extract_title


def generate_page(src: str, template: str, dest: str, basepath: str = "/"):
    print(f"Generating page from {src} to {dest} using {template}")
    
    with open(src, "r", encoding="utf-8") as f:
        markdown_content = f.read()
        
    with open(template, "r", encoding="utf-8") as f:
        template_content = f.read()
        
    html_content = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)
    
    full_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')
    
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    
    with open(dest, "w", encoding="utf-8") as f:
        f.write(full_html)


def generate_pages_recursive(content: str, template: str, dest: str, basepath: str = "/"):
    for entry in os.listdir(content):
        src_path = os.path.join(content, entry)
        dest_path = os.path.join(dest, entry.replace(".md", ".html") if entry.endswith(".md") else entry)

        if os.path.isdir(src_path):
            os.makedirs(dest_path, exist_ok=True)
            generate_pages_recursive(src_path, template, dest_path, basepath)
        elif entry.endswith(".md"):
            generate_page(src_path, template, dest_path, basepath)
