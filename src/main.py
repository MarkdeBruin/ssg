import os
import shutil
from src.copy_files import copy_files
from src.generate_pages import generate_pages_recursive

DIR_STATIC = "./static"
DIR_PUBLIC = "./public"
DIR_CONTENT = "./content"
TEMPLATE_FILE = "./template.html"

def main():
    if os.path.exists(DIR_PUBLIC):
        shutil.rmtree(DIR_PUBLIC)
    
    print("Copying static files…")   
    copy_files(DIR_STATIC, DIR_PUBLIC)
    
    print("\nGenerating pages…")
    generate_pages_recursive(DIR_CONTENT, TEMPLATE_FILE, DIR_PUBLIC)

if __name__ == "__main__":
    main()
