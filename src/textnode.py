from enum import Enum

class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    
class TextNode():
    def __init__(self, text: str, text_type: TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, node):
        if not isinstance(node, TextNode):
            return False
        if ( self.text == node.text and
            self.text_type == node.text_type and
            self.url == node.url
        ):
                return True
        return False
    
    def __repr__(self):
         return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
