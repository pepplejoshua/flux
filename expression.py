from syntax import *
from token import *
# the higher the precedence of the operator, the lower in the Tree it'll be. 
# 1 + 2 * 3
#      +     [2nd operation]
#     / \
#    1   *   [1st operation > higher precedence]
#       / \
#      2   3 

# 1 + 2 + 3
#        +
#       / \
#      +   3
#     / \
#    1   2 [since operators are the same, the parse tree is easier to construct]

# a base expression syntax abstract class which is of type ASyntax node

# an Expression is a node in the syntax tree
# a complex node which could be composed of tokens or other Expression types
class Expression(ASyntaxNode):
    pass

# a number expression which is both an expression and an abstract syntax node
class LiteralExpression(Expression):
    def __init__(self, token: Token ):
        self.token = token

    def nType(self):
        return TokenType.literal_expr
    
    def getchildren(self):
        return (self.token,)


# a number expression which is both an expression and an abstract syntax node
class BinaryExpression(Expression):
    def __init__(self, left: Expression, oper: Token, right: Expression):
        self.left = left
        self.oper = oper
        self.right = right

    def nType(self):
        return TokenType.bin_expr

    def getchildren(self):
        return (self.left, self.oper, self.right)

# this defines the grammar for parenthesized expressions
class ParenthesizedExpression(Expression):
    def __init__(self, left_paren: Token, expr: Expression, right_paren: Token):
        self.left_paren = left_paren
        self.expr = expr
        self.right_paren = right_paren

    def nType(self):
        return TokenType.paren_expr

    def getchildren(self):
        return (self.left_paren, self.expr, self.right_paren)