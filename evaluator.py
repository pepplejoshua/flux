from binding.boundexpression import *
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
            oper = int(self.evaluateexpression(root.operand))

            if sign == BUnaryOperatorType.identity:
                return oper
            elif sign == BUnaryOperatorType.negate:
                return -oper
            else: raise Exception(f'Unknown unary operator <{root.oper.tokentype.name}>')

        elif isinstance(root, BBinaryExpression):
            left = int(self.evaluateexpression(root.left))
            right = int(self.evaluateexpression(root.right))

            if root.oper == BBinaryOperatorType.plus:
                return left + right
            elif root.oper == BBinaryOperatorType.minus:
                return left - right
            elif root.oper == BBinaryOperatorType.multiply:
                return left * right
            elif root.oper in [BBinaryOperatorType.divide, BBinaryOperatorType.modulo]:
                if left == 0:
                    raise ZeroDivisionError()
                return left / right if root.oper == BBinaryOperatorType.divide else left % right
            elif root.oper == BBinaryOperatorType.exponent:
                return left ** right
            else:
                raise Exception(f'Unknown binary operator <{root.oper.name}>')

        else:
            raise Exception(f'Unknown node [{root.nodetype()}]')