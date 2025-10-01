import os
import shutil

def copy_directory(src: str, dst: str):
    if os.path.exists(dst):
        print(f"Deleting Directory: {dst}")
        shutil.rmtree(dst)
    os.makedirs(dst)

    def recursive_copy(src_path, dst_path):
        for item in os.listdir(src_path):
            s_item = os.path.join(src_path, item)
            d_item = os.path.join(dst_path, item)
            if os.path.isdir(s_item):
                os.makedirs(d_item)
                print(f"Created Directory: {d_item}")
                recursive_copy(s_item, d_item)
            else:
                shutil.copy2(s_item, d_item)
                print(f"Coppied File: {s_item} -> {d_item}")
    recursive_copy(src, dst)
