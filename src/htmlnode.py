class HTMLNode():
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props:
            return " ".join(f'{k}=\"{v}\"' for k,v in self.props.items())
        return None
        
    def __repr__(self):
        string = f"""
        -- HTML Node -- 
        Tag: {self.tag}
        Value: {self.value}
        Children: {self.children}
        props: {self.props_to_html()}
        """
        return string