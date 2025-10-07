import sys

from src.copystatic import copy_directory
from src.generate_page import generate_website

DIR_PATH_STATIC = "./static"
DIR_PATH_CONTENT = "./content"
DIR_PATH_PUBLIC = "./docs"
TEMPLATE_PATH = "template.html"

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_directory(DIR_PATH_STATIC, DIR_PATH_PUBLIC)
    generate_website(DIR_PATH_CONTENT, TEMPLATE_PATH, DIR_PATH_PUBLIC, basepath)

if __name__ == "__main__":
    main()
