from .syntax import *
from .tokens import *
from typing import Tuple
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

#      _
#      |
#      +   
#     / \
#    1   2 
# -2 * 3 can be parsed as:
#      _
#      |
#      *   
#     / \
#    1   3  (wrong, because binary * is ranked stronger than unary -) 
#     
#      or
#
#      *
#     / \
#    -   3 
#    |
#    1      (right due to normal mathematic operators parsing, unary - is ranked stronger than binary *)
# the lower an operand on the tree, the stronger the precedence.

# the case for assignment is different because, instead of starting binding from the left as with +, - and other operators,
# it binds from the right
# a = b = 5
#
# if binded from the left, the tree is:
#        =
#       / \
#      =   5
#     / \
#    a   b  this no sense as you will assign a to b and then b to 5
#
#  if binding from the right correctly, the tree is: 
#      =   
#     / \
#    a   =  
#       / \
#      b   5  5 is assigned to b and then b is assigned to a, as should be.



# a base expression syntax abstract class which is of type ASyntax node
# an Expression is a node in the syntax tree
# a complex node which could be composed of tokens or other Expression types
class Expression(SyntaxNode):
    pass


class LiteralExpression(Expression):
    def __init__(self, token: Token, val=None):
        self.token = token
        if val:
            self.value = val
        else:
            self.value = token.val

    def nodetype(self) -> TokenType:
        return TokenType.literal_expr 

    def getchildren(self) -> Tuple:
        return (self.token, )


class UnaryExpression(Expression):
    def __init__(self, operator: Token, operand: Expression):
        self.sign = operator
        self.operand = operand

    def nodetype(self) -> TokenType:
        return TokenType.unary_expr

    def getchildren(self) -> Tuple:
        return (self.sign, self.operand)


class NameExpression(Expression):
    def __init__(self, identifier: Token):
        self.identifier = identifier

    def nodetype(self) -> TokenType:
        return TokenType.name_expr

    def getchildren(self) -> Tuple:
        return (self.identifier, )

# unlike other binary operators, assignment is right associative
# eg:
# a + b + c is parsed as either (a + b) + c or a + (b + c) 
# addition is left or right associative
# a = b = c is only parsed a = (b = c).
class AssignmentExpression(Expression):
    def __init__(self, identifier: Token, equals: Token, expr: Expression):
        self.identifier = identifier
        self.oper = equals
        self.expr = expr

    def nodetype(self) -> TokenType:
        return TokenType.assignment_expr

    def getchildren(self) -> Tuple:
        return (self.identifier, self.equals, self.expr)


class BinaryExpression(Expression):
    def __init__(self, left: Expression, oper: Token, right: Expression):
        self.left = left
        self.oper = oper
        self.right = right

    def nodetype(self) -> TokenType:
        return TokenType.bin_expr

    def getchildren(self) -> Tuple:
        return (self.left, self.oper, self.right)


# this defines the grammar for parenthesized expressions
class ParenthesizedExpression(Expression):
    def __init__(self, left_paren: Token, expr: Expression, right_paren: Token):
        self.left_paren = left_paren
        self.expr = expr
        self.right_paren = right_paren

    def nodetype(self) -> TokenType:
        return TokenType.paren_expr

    def getchildren(self):
        return (self.left_paren, self.expr, self.right_paren)