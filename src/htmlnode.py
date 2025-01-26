class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        props = ""
        for key in self.props:
            props = props + f' {key}="{self.props[key]}"'
        return props
    
    def __repr__(self):
        if self.tag != None and self.value != None and self.children != None and self.props != None:
            return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
        
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=[], props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Value should have a value")
        if self.tag == None:
            return f"{self.value}"
        if self.props is not None:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag should have a value")
        if self.children is None:
            raise ValueError("There should be children assigned to this parent node")
        if self.props:
            opening_tag = f"<{self.tag}{self.props_to_html()}>"
        else:
            opening_tag = f"<{self.tag}>"
        children_html = "".join(child.to_html() for child in self.children)
        return f"{opening_tag}{children_html}</{self.tag}>"