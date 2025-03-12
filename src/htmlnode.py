


class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        props_str_list = []
        props_tuples = self.props.items()
        for prop_tuple in props_tuples:
            props_str_list.append(f"{prop_tuple[0]}={prop_tuple[1]}")
        res = " ".join(props_str_list)
        return res

    def __repr__(self):
        return self.tag, self.value, self.children, self.props
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value is None:
            raise ValueError("LeafNode must have a value")
        super().__init__(tag = tag, value=value, children=None, props=props)
    def to_html(self):
        if self.value is None:
            return ValueError("LeafNode must have a value")
        if self.tag is None:
            return self.value
        else:
            return (f"<{self.tag}>{self.value}</{self.tag}>")
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        if tag is None:
            raise ValueError("ParentNode must have tag(s)")
        if children is None:
            raise ValueError("ParentNode must have children")          
        super().__init__(tag = tag, children = children, props = props)      

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have tag(s)")
        if self.children is None:
            raise ValueError("ParentNode must have children")

        res = ""

        if isinstance(self, ParentNode):
            parent_and_children_str = f"<{self.tag}>" # opening parent tag
            for child in self.children: # parent must have children, so this will not fail
                parent_and_children_str += child.to_html()
            parent_and_children_str += f"</{self.tag}>"
            res += parent_and_children_str # closing parent tag
        
        return res
        
             
            

