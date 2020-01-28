from enum import Enum, auto
from .boundoperatortypes import *
from .boundnode import BoundNode
from abc import abstractmethod

# the various bound expression types
class BNodeType(Enum):
    bLiteral_expr = auto()
    bUnary_expr = auto()
    bBin_expr = auto()

# this is the base bound expression type
class BExpression(BoundNode): 
    @abstractmethod
    # this returns the bound expression type
    def type(self):
        pass

class BLiteralExpression(BExpression):
    def __init__(self, val):
        self.value = val

    # this is the type of BNode [Expression type]
    def nodetype(self) -> BNodeType:
        return BNodeType.bLiteral_expr
    
    # this is the actual typing used for type checking.
    # this is the type that the expression results to
    def type(self):
        return type(self.value)

class BUnaryExpression(BExpression):
    def __init__(self, oper: BUnaryOperatorType, operand: BExpression):
        self.sign = oper
        self.operand = operand
    
    # this is the type of BoundNode [Expression type]
    def nodetype(self) -> BNodeType:
        return BNodeType.bUnary_expr
    
    # this is the actual typing used for type checking
    # this is the type that the expression results to+
    def type(self):
        return self.operand.type()

class BBinaryExpression(BExpression):
    def __init__(self, left: BExpression, oper: BBinaryOperatorType, right: BExpression):
        self.left = left
        self.oper = oper
        self.right = right
  
    # this is the type of BoundNode [Expression type]
    def nodetype(self) -> BNodeType:
        return BNodeType.bBin_expr
    
    # this is the actual typing used for type checking
    # this is the type that the expression results to
    def type(self):
        return self.left.type()