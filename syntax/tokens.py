from termcolor import cprint
from .syntax import SyntaxNode
from .tokentype import TokenType
# by making Token class inherit the Abstract Syntax node, they become the building blocks of either simple 
# or complex syntax nodes. They are the leaves of the syntax tree
class Token(SyntaxNode):
    def __init__(self, token_type, pos, val=None):
        self.tokentype = token_type
        self.val = val
        self.pos = pos

    def nodetype(self):
        return self.tokentype

    # it is a leaf
    def getchildren(self):
        return ()

    def display(self):
        """Print a formatted Token"""
        print(f"<Value: {self.val}, Token Type: {self.token_t.name}, Pos: {self.pos}>")