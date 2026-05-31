import re
from enum import Enum
from textnode import TextNode, TextType


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