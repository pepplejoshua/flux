from termcolor import cprint
from .syntax import SyntaxNode
from .tokentype import TokenType
from typing import Tuple
# by making Token class inherit the Abstract Syntax node, they become the building blocks of either simple 
# or complex syntax nodes. They are the leaves of the syntax tree
class Token(SyntaxNode):
    def __init__(self, token_type, pos, val=None):
        self.tokentype = token_type
        self.val = val
        self.pos = pos

    def nodetype(self) -> TokenType:
        return self.tokentype

    # it is a leaf
    def getchildren(self) -> Tuple:
        return ()

    def display(self):
        """Print a formatted Token"""
        print(f"<Value: {self.val}, Token Type: {self.tokentype.name}, Pos: {self.pos}>")