class HTMLNode:
  def __init__(self, tag=None, value=None, children=None, props=None):
    self.tag = tag
    self.value = value
    self.children = children if children else []
    self.props = props
    
  def to_html(self):
    if self.value:
      return f"<{self.tag}>{self.value}</{self.tag}>"
    else:
      # Convert children properly into HTML strings
      children_html = ''.join(child.to_html() for child in self.children)
      return f"<{self.tag}>{children_html}</{self.tag}>"
  
  def props_to_html(self):
    if not self.props:
      return ''
    props_string = ''
    for prop in self.props:
      props_string += f' {prop}="{self.props[prop]}"'
      
    return props_string
  
  def __eq__(self, other):
    if isinstance(other, HTMLNode):
      return (
        self.tag == other.tag and
        self.value == other.value and
        self.children == other.children and
        self.props == self.props
      )
      
    return False
  
  def __repr__(self):
    return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
  
class LeafNode(HTMLNode):
  def __init__(self, tag=None, value=None, props=None):
    super().__init__(tag, value, None, props)

  def to_html(self):
    if self.value is None:
      raise ValueError("Invalid HTML: no value")
    if self.tag is None:
      return self.value
    return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
  
  def __eq__(self, other):
    if isinstance(other, LeafNode):
      return (
        self.tag == other.tag and
        self.value == other.value and
        self.props == other.props
      )
    return False

  def __repr__(self):
    return f"LeafNode({self.tag}, {self.value}, {self.props})"
  
class ParentNode(HTMLNode):
  def __init__(self, tag, children, props=None):
    super().__init__(tag, None, children, props)
    
  def to_html(self):
    if not self.tag:
      raise ValueError("Invalid HTML: no tag")
    if not self.children:
      raise ValueError("Invalid HTML: no children")
    children_html = "".join(child.to_html() for child in self.children)
    
    return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
  
  def __eq__(self, other):
    if isinstance(other, ParentNode):
      return (
        self.tag == other.tag and
        self.children == other.children and
        self.props == self.props
      )
      
    return False
  
  def __repr__(self):
    return f"ParentNode({self.tag}, {self.children}, {self.props})"