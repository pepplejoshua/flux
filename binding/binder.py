# effectively a type checker
import sys
sys.path.append('..')
from syntax.expression import *
from .boundexpression import *
from .bbinaryoperator import *
from .bunaryoperator import *
from syntax.tokentype import TokenType

class Binder:
    def __init__(self):
        self.diagnostics = []

    # entry point for recursion, similar to parser structure
    # depending on Expression type, we bind differently
    def bindexpression(self, expr: Expression) -> BExpression:
        if expr.nodetype() == TokenType.literal_expr:
            return self.bindliteralexpression(expr)
        elif expr.nodetype() == TokenType.unary_expr:
            return self.bindunaryexpression(expr)
        elif expr.nodetype() == TokenType.bin_expr:
            return self.bindbinaryexpression(expr)
        elif expr.nodetype() == TokenType.paren_expr:
            return self.bindexpression(expr.expr)
        else: 
            raise Exception(f"Unexpected syntax {expr.nodetype()}")

        # LITERALS
    def bindliteralexpression(self, expr: LiteralExpression) -> BLiteralExpression:
        if isinstance(expr.value, bool):
            return BLiteralExpression(expr.value)
        else:
            try:
                val = int(expr.value)  
            except ValueError:
                val = 0
        return BLiteralExpression(val)

        # UNARY
    def bindunaryexpression(self, expr: UnaryExpression) -> BUnaryExpression:
        b_operand = self.bindexpression(expr.operand)
        b_sign = BUnaryOperator.bind(expr.sign.tokentype, b_operand.type())
        if not b_sign:
            self.diagnostics.append(f"Unary operator {expr.sign.val} not defined for type {b_operand.type()}.")
            return b_operand
        return BUnaryExpression(b_sign, b_operand)

        # BINARY
    def bindbinaryexpression(self, expr: BinaryExpression) -> BBinaryExpression:
        b_left = self.bindexpression(expr.left) 
        b_right = self.bindexpression(expr.right)
        b_sign = BBinaryOperator.bind(expr.oper.tokentype, b_left.type(), b_right.type())
        if not b_sign: 
            self.diagnostics.append(f"Binary operator {expr.oper.val} not defined for types {b_left.type()} and {b_right.type()}.")
            return b_left
        return BBinaryExpression(b_left, b_sign, b_right)