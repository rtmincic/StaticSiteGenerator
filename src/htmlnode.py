

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        props = ""
        for key in self.props:
            props = props + f' {key}="{self.props[key]}"'
        return props
    
    def __repr__(self):
        if self.tag != None and self.value != None and self.children != None and self.props != None:
            return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
        
        
        