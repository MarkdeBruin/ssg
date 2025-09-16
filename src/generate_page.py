import os
from src.md_to_html import markdown_to_html_node
from src.md_meta import extract_title


def generate_page(src: str, template: str, dst: str):
    print(f"Generating page from {src} to {dst} using {template}")
    
    with open(src, "r", encoding="utf-8") as f:
        markdown_content = f.read()
        
    with open(template, "r", encoding="utf-8") as f:
        template_content = f.read()
        
    html_content = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)
    
    full_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    
    with open(dst, "w", encoding="utf-8") as f:
        f.write(full_html)
