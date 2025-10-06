from src.copystatic import copy_directory
from src.generate_page import generate_page, generate_website

DIR_PATH_STATIC = "./static"
DIR_PATH_CONTENT = "./content"
DIR_PATH_PUBLIC = "./public"
TEMPLATE_PATH = "template.html"

def main():
    copy_directory(DIR_PATH_STATIC, DIR_PATH_PUBLIC)
    generate_website(DIR_PATH_CONTENT, TEMPLATE_PATH, DIR_PATH_PUBLIC)

if __name__ == "__main__":
    main()
