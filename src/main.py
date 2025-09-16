import os, shutil
from copy_files import copy_files

DIR_STATIC = "./static"
DIR_PUBLIC = "./public"

def main():
    if os.path.exists(DIR_PUBLIC):
        shutil.rmtree(DIR_PUBLIC)
    
    print("Copying files…")   
    copy_files(DIR_STATIC, DIR_PUBLIC)
    print("Done copying") 

if __name__ == "__main__":
    main()
