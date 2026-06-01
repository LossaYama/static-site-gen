import os
import shutil
import sys
from markdown import markdown_to_html_node, extract_title
from htmlnode import HTMLNode

def main():
    basepath = sys.argv[1]
    if basepath == "":
        basepath = "/"
    target_dir = "docs"
    # delete current content of target dir or creates target dir
    if os.path.isdir(target_dir):
        shutil.rmtree(target_dir)
    os.mkdir(target_dir)
    copy_source_to_target("static", target_dir)
    generate_pages_recursive("content", "template.html", target_dir, basepath)

def copy_source_to_target(from_path: str, dest_path: str):
    # copy contents from source to target
    if os.path.isdir(from_path):
        contents = os.listdir(from_path)
        for content in contents:
            path = os.path.join(from_path, content)
            if os.path.isfile(path):
                shutil.copy(path, dest_path)
            elif os.path.isdir(path):
                dir_to_target = os.path.join(dest_path, content)
                if not os.path.exists(dir_to_target):
                    os.mkdir(dir_to_target)
                copy_source_to_target(path, dir_to_target) 
    else:
        raise Exception("source directory does not exist or is not a directory")

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str):
    print(f"Generating pages from {dir_path_content} to {dest_dir_path} using {template_path}")
    items = os.listdir(dir_path_content)
    for item in items:
        from_path = os.path.join(dir_path_content, item)
        if os.path.isfile(from_path):
            dest_path = os.path.join(dest_dir_path, item.removesuffix(".md")+".html")
            generate_page(from_path, template_path, dest_path, basepath)           
        else:
            next_dir_path = os.path.join(dir_path_content, item)
            next_dest_path = os.path.join(dest_dir_path, item)
            generate_pages_recursive(next_dir_path, template_path, next_dest_path, basepath)

def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file:
        content = file.read()
    with open(template_path) as file:
        template = file.read()
    html_node = markdown_to_html_node(content)
    content_html = html_node.to_html()
    title = extract_title(content)
    para_page1 = template.replace("{{ Title }}", title)
    para_page2 = para_page1.replace("{{ Content }}", content_html)
    para_page3 = para_page2.replace('href="/', f'href="{basepath}')
    page = para_page3.replace('src="/', f'src="{basepath}')
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    with open(dest_path, "w") as file:
        file.write(page)


if __name__ == "__main__":
    main()