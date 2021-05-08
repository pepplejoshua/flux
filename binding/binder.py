# effectively a type checker
from Core.expression import *
from .boundexpression import *
from .bbinaryoperator import *
from .bunaryoperator import *
from Core.tokentype import TokenType
from Core.diagnostics import DiagnosticsBag
from Core.variablesym import VariableSym

class Binder:
    def __init__(self, variables):
        self.diagnostics = DiagnosticsBag()
        self.variables = variables 
        self.error = False

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
        if not self.error:
            b_operand = self.bindexpression(expr.operand)
            b_sign = BUnaryOperator.bind(expr.sign.tokentype, b_operand.type())
            if not b_sign:
                self.diagnostics.reportundefinedunaryoperator(expr.sign.span(), expr.sign.val, b_operand.type())
                self.error = True
                return b_operand
            return BUnaryExpression(b_sign, b_operand)

        # BINARY
    def bindbinaryexpression(self, expr: BinaryExpression) -> BBinaryExpression:
        if not self.error:
            b_left = self.bindexpression(expr.left) 
            b_right = self.bindexpression(expr.right)
            
            b_sign = BBinaryOperator.bind(expr.oper.tokentype, b_left.type(), b_right.type())
            if not b_sign: 
                self.diagnostics.reportundefinedbinaryoperator(expr.oper.span(), expr.oper.val, b_left.type(), b_right.type())
                self.error = True
                return b_left
            return BBinaryExpression(b_left, b_sign, b_right)

    def bindparenthesizedexpression(self, expr: ParenthesizedExpression) -> BExpression:
        if not self.error:
            return self.bindexpression(expr.expr)

    def boundvariableslookup(self, varStr: str) -> VariableSym:
        if not self.error:
            var = None
            for vSym in self.variables:
                if vSym.name == varStr:
                    var = vSym
                    break
            return var

    def bindnameexpression(self, expr: NameExpression) -> BExpression:
        if not self.error:
            name = expr.identifier.val
            var = self.boundvariableslookup(name)
            if not var:
                self.diagnostics.reportundefinedname(expr.identifier.span(), name)
                self.error = True
                # undefined variables currently always return a 0 literal
                return BLiteralExpression(0)
            
            # ############################################# #
            return BVariableExpression(var)

    def bindassignmentexpression(self, expr: AssignmentExpression) -> BExpression:
        name = expr.identifier.val
        bExpr = self.bindexpression(expr.expr)
        
        if not self.error:
            var = self.boundvariableslookup(name)
            if not var:
                defaultV = None
                # this creates a default binding in the variables dict before
                # initialization is done by the evaluator
                # in the case where the variable exists though, we end up overwriting it,
                # so I introduced the wrapping if statement to detect already existing variables
                if (bExpr.type() == int):
                    defaultV = 0
                elif (bExpr.type() == bool):
                    defaultV = False

                if defaultV == None:
                    raise Exception(f"Unsupported variable type: {bExpr.type()}")
                varSym = VariableSym(name, bExpr.type())
                self.variables[varSym] = defaultV
                return BAssignmentExpression(varSym, bExpr)
            return BAssignmentExpression(var, bExpr)
        