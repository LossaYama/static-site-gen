from textnode import TextNode, TextType


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
                raise Exception("invalid markdown syntax, delimiter count is not even")
    return new_nodes