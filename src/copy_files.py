import os, shutil


def copy_files(src: str, dst: str):
    os.makedirs(dst, exist_ok=True)
    
    for filename in os.listdir(src):
        src_path = os.path.join(src, filename)
        dst_path = os.path.join(dst, filename)
    
        if os.path.isdir(src_path):
            copy_files(src_path, dst_path)
        else:
            shutil.copy(src_path, dst_path)
            print(f" * Copied file: {src_path} -> {dst_path}")