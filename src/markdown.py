import re
from enum import Enum
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, ParentNode


# TEXT FORMATTING PROCESSING
def text_to_textnodes(text:str) -> list[TextNode]:
    textnodes = [TextNode(text, TextType.TEXT),]
    textnodes = split_nodes_delimiter(textnodes, "**", TextType.BOLD)
    textnodes = split_nodes_delimiter(textnodes, "_", TextType.ITALIC)
    textnodes = split_nodes_delimiter(textnodes, "`", TextType.CODE)
    textnodes = split_nodes_image(textnodes)
    textnodes = split_nodes_link(textnodes)
    return textnodes

def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
    ) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_text = node.text.split(delimiter)
            if len(split_text) % 2 == 1:
                for i in range(len(split_text)):
                    if split_text[i] == "":
                        continue
                    elif i == 0 or i % 2 == 0:
                        new_nodes.append(TextNode(split_text[i], TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(split_text[i], text_type))                
            else:
                raise Exception("invalid markdown syntax")
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("#"):
            if not line.startswith("##"):
                return line.lstrip("#").strip()
    raise Exception("no header found")

def extract_markdown_images(text:str) -> list[tuple[str,str]]:
    # [( thing after ! and in [], thing in () ), ...]
    # * lets it select 0 or more
    # [^...] makes it drop the brackets when records the string
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text:str) -> list[tuple[str,str]]:
    # first section makes sure it doesn't pick up images
    # then [( thing in [], thing in () ), ...]
    # rest same as above
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


# BLOCKS PROCESSING
def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    clean_blocks = []
    for block in blocks:
        clean_block = block.strip()
        if clean_block != "":
            clean_blocks.append(clean_block)
    return clean_blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def block_to_blocktype(md_block: str) -> "BlockType":
    if md_block.startswith("# ") or md_block.startswith("## ") or md_block.startswith("### ") or md_block.startswith("#### ") or md_block.startswith("##### ") or md_block.startswith("###### "):
        return BlockType.HEADING
    elif md_block.startswith("```\n") and md_block.endswith("```"):
        return BlockType.CODE
    else:
        lines = md_block.split("\n")
        quote = True
        unordered = True
        ordered = True
        count = 1
        for line in lines:
            if not line.startswith(">"):
                quote = False
            if not line.startswith("- "):
                unordered = False
            if not line.startswith(f"{count}. "):
                ordered = False
            count += 1
        if quote:
            return BlockType.QUOTE
        elif unordered:
            return BlockType.UNORDERED_LIST
        elif ordered:
            return BlockType.ORDERED_LIST
        else:
            return BlockType.PARAGRAPH
        

# MARKDOWN TO HTML
def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_blocktype(block)
        if block_type is BlockType.QUOTE:
            lines = block.split("\n")
            stripped_lines = []
            for line in lines:
                stripped_lines.append(line.lstrip(">").strip())
            text = " ".join(stripped_lines)
            para_children = text_to_children(text)
            children.append(ParentNode("blockquote", para_children))
        elif block_type is BlockType.UNORDERED_LIST:
            list_items = block.split("\n")
            unordered_children = []
            for item in list_items:
                text = item.strip("- ")
                para_children = text_to_children(text)
                unordered_children.append(ParentNode("li", para_children))
            children.append(ParentNode("ul", unordered_children))
        elif block_type is BlockType.ORDERED_LIST:
            list_items = block.split("\n")
            ordered_children = []
            for item in list_items:
                text = item[3:]
                para_children = text_to_children(text)
                ordered_children.append(ParentNode("li", para_children))
            children.append(ParentNode("ol", ordered_children))
        elif block_type is BlockType.CODE:
            text = block[3:-3].removeprefix("\n")
            text_node = TextNode(text, TextType.TEXT)
            html_node = text_node_to_html_node(text_node)
            para_children = ParentNode("code", [html_node])
            children.append(ParentNode("pre", [para_children]))
        elif block_type is BlockType.HEADING:
            header_number = block[:6].count("#")
            text = block.strip("# ")
            para_children = text_to_children(text)
            children.append(ParentNode(f"h{header_number}", para_children))
        elif block_type is BlockType.PARAGRAPH:
            text = block.replace("\n", " ")
            para_children = text_to_children(text)  # returns a list of inline HTMLNodes
            children.append(ParentNode("p", para_children))
        else:
            raise Exception("invalid block type")
    return ParentNode("div", children)

def text_to_children(text: str) -> list:
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes