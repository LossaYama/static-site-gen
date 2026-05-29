from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        same_text = self.text == other.text
        same_type = self.text_type == other.text_type
        same_url = self.url == other.url
        return same_text and same_type and same_url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"