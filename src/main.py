import os
import shutil
from markdown import markdown_to_html_node, extract_title
from htmlnode import HTMLNode

def main():
    source = "static"
    target = "public"
    # delete current content of target dir or creates target dir
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.mkdir(target)
    copy_source_to_target(source, target)
    generate_page("content/index.md", "template.html", "public/index.html")

def copy_source_to_target(source: str, target: str):
    # copy contents from source to target
    if os.path.isdir(source):
        contents = os.listdir(source)
        for content in contents:
            path = os.path.join(source, content)
            if os.path.isfile(path):
                shutil.copy(path, target)
            elif os.path.isdir(path):
                dir_to_target = os.path.join(target, content)
                if not os.path.exists(dir_to_target):
                    os.mkdir(dir_to_target)
                copy_source_to_target(path, dir_to_target) 
    else:
        raise Exception("source directory does not exist or is not a directory")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file:
        content = file.read()
    with open(template_path) as file:
        template = file.read()
    html_node = markdown_to_html_node(content)
    content_html = html_node.to_html()
    title = extract_title(content)
    para_page = template.replace("{{ Title }}", title)
    page = para_page.replace("{{ Content }}", content_html)
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    with open(dest_path, "w") as file:
        file.write(page)

if __name__ == "__main__":
    main()