class HTMLNode:
    def __init__(
        self,
        tag: str = None,
        value: str = None,
        children: list = None,
        props: dict = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props:
            return " " + " ".join(f'{k}="{v}"' for k, v in self.props.items())
        return ""

    def __repr__(self):
        string = f"""
        -- HTML Node -- 
        Tag: {self.tag}
        Value: {self.value}
        Children: {self.children}
        props: {self.props_to_html()}
        """
        return string


class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props:dict=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            return ValueError("LeafNode with no value")

        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: dict=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            return ValueError("ParentNode with no tag")

        if not self.children:
            return ValueError("ParentNode missing children")

        results = ""
        for child in self.children:
            result = child.to_html()
            if not isinstance(
                result, ValueError
            ):
                results += result
            else:
                return ValueError(str(result))
        return f"<{self.tag}>{results}</{self.tag}>"
