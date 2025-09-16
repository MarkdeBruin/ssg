import os, sys
import shutil
from src.copy_files import copy_files
from src.generate_pages import generate_pages_recursive

DIR_STATIC = "./static"
DIR_PUBLIC = "./docs"
DIR_CONTENT = "./content"
TEMPLATE_FILE = "./template.html"

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    
    if os.path.exists(DIR_PUBLIC):
        shutil.rmtree(DIR_PUBLIC)
    
    print("Copying static files…")   
    copy_files(DIR_STATIC, DIR_PUBLIC)
    
    print("\nGenerating pages…")
    generate_pages_recursive(DIR_CONTENT, TEMPLATE_FILE, DIR_PUBLIC, basepath)

if __name__ == "__main__":
    main()
