from abc import ABC, abstractmethod

# a base node type for syntax tree
class ASyntaxNode(ABC):
    @abstractmethod
    def nType(self):
        pass

    @abstractmethod
    def getchildren(self):
        pass

# a syntax tree class which is just a class containing a root to attached ASyntaxNode(s)
class SyntaxTree:
    def __init__(self, diagnostic, root, eof_token):
        self.diag = diagnostic
        self.root = root
        self.eof = eof_token