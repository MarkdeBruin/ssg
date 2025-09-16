import os, shutil
from src.copy_files import copy_files
from src.generate_page import generate_page

DIR_STATIC = "./static"
DIR_PUBLIC = "./public"
DIR_CONTENT = "./content"
TEMPLATE_FILE = "./template.html"

INDEX_MD = os.path.join(DIR_CONTENT, "index.md")
INDEX_HTML = os.path.join(DIR_PUBLIC, "index.html")

def main():
    if os.path.exists(DIR_PUBLIC):
        shutil.rmtree(DIR_PUBLIC)
    
    print("Copying files…")   
    copy_files(DIR_STATIC, DIR_PUBLIC)
    print("\n\n") 
    
    generate_page(INDEX_MD, TEMPLATE_FILE, INDEX_HTML)

if __name__ == "__main__":
    main()
