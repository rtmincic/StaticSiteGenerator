import os
import shutil

def copy_static_to_public():
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")
    copy_directory("static", "public")

def copy_directory(source_path, dest_path):
    files = os.listdir(source_path)
    for file in files:
        source_item = os.path.join(source_path, file)
        dest_item = os.path.join(dest_path, file)
        if os.path.isfile(source_item):
            shutil.copy(source_item, dest_item)
        else:
            os.mkdir(dest_item)
            copy_directory(source_item, dest_item)