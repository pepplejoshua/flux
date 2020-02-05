from binding.boundexpression import *
from binding.boundoperatortypes import *


# this recursively traverses a bound tree[SyntaxTree] and returns a result
class BExpressionEvaluator:
    def __init__(self, rootExpr: BExpression):
        self.root = rootExpr
    
    def evaluate(self):
        return self.evaluateexpression(self.root)

    def evaluateexpression(self, root: BExpression):
        # separate case for separate expression types 
        # num_expr, bin_expr, unary_expr, paren_expr
        
        if isinstance(root, BLiteralExpression):
            return root.value  

        elif isinstance(root, BUnaryExpression):
            sign = root.sign
            oper = self.evaluateexpression(root.operand)

            if sign.operatortype == BUnaryOperatorType.identity:
                return int(oper)
            elif sign.operatortype == BUnaryOperatorType.negate:
                return -int(oper)
            elif sign.operatortype == BUnaryOperatorType.log_negate:
                return not bool(oper)
            else: raise Exception(f'Unknown unary operator <{root.sign.operatortype.name}>')

        elif isinstance(root, BBinaryExpression): 
            left = self.evaluateexpression(root.left)
            right = self.evaluateexpression(root.right)
            
            if root.oper.operatortype == BBinaryOperatorType.plus:
                return int(left) + int(right)
            elif root.oper.operatortype == BBinaryOperatorType.minus:
                return int(left) - int(right)
            elif root.oper.operatortype == BBinaryOperatorType.multiply:
                return int(left) * int(right)
            elif root.oper.operatortype in [BBinaryOperatorType.divide, BBinaryOperatorType.modulo]:
                if left == 0:
                    raise ZeroDivisionError()
                return int(int(left) / int(right)) if root.oper.operatortype == BBinaryOperatorType.divide else int(int(left) % int(right))
            elif root.oper.operatortype == BBinaryOperatorType.exponent:
                return int(left) ** int(right)
            elif root.oper.operatortype == BBinaryOperatorType.log_and:
                return bool(left) and bool(right)
            elif root.oper.operatortype == BBinaryOperatorType.log_or:
                return bool(left) or bool(right)
            elif root.oper.operatortype == BBinaryOperatorType.equal:
                return left == right
            elif root.oper.operatortype == BBinaryOperatorType.notequal:
                return not(left == right)
            else:
                raise Exception(f'Unknown binary operator <{root.oper.operatortype.name}>')

        else:
            raise Exception(f'Unknown node [{root.nodetype()}]')