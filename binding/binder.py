# effectively a type checker
import sys
sys.path.append('..')
from syntax.expression import *
from .boundexpression import *
from .bbinaryoperator import *
from .bunaryoperator import *
from syntax.tokentype import TokenType
from textspan import TextSpan
<<<<<<< HEAD
from diagnostics import DiagnosticBag

class Binder:
    def __init__(self):
        self.Diagnostics = DiagnosticBag()
    
=======
from diagnostics import DiagnosticsBag

class Binder:
    def __init__(self):
        self.diagnostics = DiagnosticsBag()

>>>>>>> c8712e7da967f336c28cd1698865615c7e3a890c
    # entry point for recursion, similar to parser structure
    # depending on Expression type, we bind differently
    # this is ordered by Immo's precedence. 
    # TODO: try other arrangements
    def bindexpression(self, expr: Expression) -> BExpression:
        if expr.nodetype() == TokenType.paren_expr:
            return self.bindparenthesizedexpression(expr)
        elif expr.nodetype() == TokenType.literal_expr:
            return self.bindliteralexpression(expr)
        elif expr.nodetype() == TokenType.name_expr:
            return self.bindnameexpression(expr)
        elif expr.nodetype() == TokenType.assignment_expr:
            return self.bindassignmentexpression(expr)
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
        b_sign = BUnaryOperator.bind(expr.sign.tokentype, b_operand.type())
        if not b_sign:
<<<<<<< HEAD
            self.Diagnostics.reportundefinedunaryoperator(expr.sign.span(), expr.sign.val, b_operand.type())
=======
            self.diagnostics.reportundefinedunaryoperator(expr.sign.span(), expr.sign.val, b_operand.type())
>>>>>>> c8712e7da967f336c28cd1698865615c7e3a890c
            return b_operand
        return BUnaryExpression(b_sign, b_operand)

        # BINARY
    def bindbinaryexpression(self, expr: BinaryExpression) -> BBinaryExpression:
        b_left = self.bindexpression(expr.left) 
        b_right = self.bindexpression(expr.right)
        b_sign = BBinaryOperator.bind(expr.oper.tokentype, b_left.type(), b_right.type())
        if not b_sign: 
<<<<<<< HEAD
            self.Diagnostics.reportundefinedbinaryoperator(expr.oper.span(), expr.oper.val, b_left.type(), b_right.type())
=======
            self.diagnostics.reportundefinedbinaryoperator(expr.oper.span(), expr.oper.val, b_left.type(), b_right.type())
>>>>>>> c8712e7da967f336c28cd1698865615c7e3a890c
            return b_left
        return BBinaryExpression(b_left, b_sign, b_right)

    def bindparenthesizedexpression(self, expr: ParenthesizedExpression) -> BExpression:
        return self.bindexpression(expr.expr)

    def bindnameexpression(self, expr: NameExpression) -> BExpression:
        pass

    def bindassignmentexpression(self, expr: AssignmentExpression) -> BExpression:
        pass