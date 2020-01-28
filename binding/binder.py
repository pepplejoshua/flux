# effectively a type checker
import sys
sys.path.append('..')
from syntax.expression import *
from .boundexpression import *
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
        b_sign = self.bindunaryoperatortype(expr.sign.tokentype, b_operand.type())
        if not b_sign:
            self.diagnostics.append(f"Unary operator {expr.sign.val} not defined for type {b_operand.type()}.")
            return b_operand
        return BUnaryExpression(b_sign, b_operand)

        # BINARY
    def bindbinaryexpression(self, expr: BinaryExpression) -> BBinaryExpression:
        b_left = self.bindexpression(expr.left) 
        b_right = self.bindexpression(expr.right)
        b_sign = self.bindbinaryoperatortype(expr.oper.tokentype, b_left.type(), b_right.type())
        if not b_sign:
            self.diagnostics.append(f"Binary operator {expr.oper.val} not defined for types {b_left.type()} and {b_right.type()}.")
            return b_left
        return BBinaryExpression(b_left, b_sign, b_right)

        # used for type checking and binding unary operators and operand to the same type
    def bindunaryoperatortype(self, token_type: TokenType, op_type: type) -> BUnaryOperatorType:
        if op_type != int:
            return None
        ops = {
            TokenType.plus: BUnaryOperatorType.identity,
            TokenType.minus: BUnaryOperatorType.negate
        }
        op_t = ops[token_type]
        if op_t:
            return op_t
        else:
            raise Exception(f"Unexpected unary operator {expr.nodetype()}")
        
        # used for type checking and binding binary operators and operands to the same type
    def bindbinaryoperatortype(self, token_type: TokenType, lo_type: type, ro_type: type) -> BBinaryOperatorType:
        if lo_type != int or ro_type != int:
            return None
        ops = {
            TokenType.plus: BBinaryOperatorType.plus,
            TokenType.minus: BBinaryOperatorType.minus,
            TokenType.multiply: BBinaryOperatorType.multiply,
            TokenType.divide: BBinaryOperatorType.divide,
            TokenType.modulo: BBinaryOperatorType.modulo, 
            TokenType.exponent: BBinaryOperatorType.exponent,
            TokenType.assignment: BBinaryOperatorType.assignment 
        }
        op_type = ops[token_type]
        if op_type:
            return op_type
        else:
            raise Exception(f"Unexpected binary operator {expr.nodetype()}")
        