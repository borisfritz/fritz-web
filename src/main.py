from src.copystatic import copy_directory
from src.generate_page import generate_page

DIR_PATH_STATIC = "./static"
DIR_PATH_PUBLIC = "./public"
TEMPLATE_PATH = "template.html"

def main():
    copy_directory(DIR_PATH_STATIC, DIR_PATH_PUBLIC)
    generate_page("content/index.md", TEMPLATE_PATH, "public/index.html")

if __name__ == "__main__":
    main()
