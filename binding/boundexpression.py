from Core.variablesym import VariableSym
from enum import Enum, auto
from .bbinaryoperator import BBinaryOperator
from .bunaryoperator import BUnaryOperator
from .boundnode import BoundNode
from abc import abstractmethod

# the various bound expression types
class BNodeType(Enum):
    bLiteral_expr = auto()
    bUnary_expr = auto()
    bBin_expr = auto()
    bVariable_expr = auto()
    bAssignment_expr = auto()

# this is the base bound expression type
class BExpression(BoundNode): 
    @abstractmethod
    # this returns the bound expression type
    def nodetype(self) -> BNodeType:
        pass
    
    @abstractmethod
    # this returns the bound expression type
    def type(self):
        pass

    @abstractmethod
    # this returns the primitive contents of the bound expression type
    def composition(self):
        pass

class BLiteralExpression(BExpression):
    def __init__(self, val):
        self.value = val

    # this is the type of BNode [Expression type]
    def nodetype(self) -> BNodeType:
        return BNodeType.bLiteral_expr
    
    # this is the actual typing used for type checking.
    # this is the type that the expression results to
    def type(self) -> type:
        return type(self.value)

    def composition(self):
        return (self.value, )

class BUnaryExpression(BExpression):
    def __init__(self, oper: BUnaryOperator, operand: BExpression):
        self.sign = oper
        self.operand = operand
    
    # this is the type of BoundNode [Expression type]
    def nodetype(self) -> BNodeType:
        return BNodeType.bUnary_expr
    
    # this is the actual typing used for type checking
    # this is the type that the expression results to, hence should be the actual operator's type
    def type(self) -> type:
        return self.sign.resulttype

    def composition(self):
        return (self.sign, self.operand)
        
class BBinaryExpression(BExpression):
    def __init__(self, left: BExpression, oper: BBinaryOperator, right: BExpression):
        self.left = left
        self.oper = oper
        self.right = right
  
    # this is the type of BoundNode [Expression type]
    def nodetype(self) -> BNodeType:
        return BNodeType.bBin_expr
    
    # this is the actual typing used for type checking
    # this is the type that the expression results to
    def type(self) -> type:
        return self.oper.resulttype

    def composition(self):
        return (self.left, self.oper, self.right)

class BVariableExpression(BExpression):
    def __init__(self, varSym: VariableSym):
        self.variable = varSym

    def nodetype(self) -> BNodeType:
        return BNodeType.bVariable_expr

    def type(self) -> type:
        return self.variable.typing

    def composition(self):
        return (self.variable)

class BAssignmentExpression(BExpression):
    def __init__(self, varSym: VariableSym, bExpr: BExpression):
        self.variable = varSym
        self.expression = bExpr

    def nodetype(self) -> BNodeType:
        return BNodeType.bAssignment_expr

    def type(self) -> type:
        return self.expression.type()
        
    def composition(self):
        return (self.variable, self.expression)