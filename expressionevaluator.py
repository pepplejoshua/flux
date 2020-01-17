from expression import *
# this recursively traverses a parse tree[SyntaxTree] and returns a result
class ExpressionEvaluator:
    def __init__(self, rootExpr):
        self.root = rootExpr
    
    def evaluate(self):
        return self.evaluateexpression(self.root)

    def evaluateexpression(self, root):
        # separate case for separate expression types 
        # num_expr, bin_expr
        
        if isinstance(root, NumberExpression):
            return root.token.val
        elif isinstance(root, BinaryExpression):
            left = self.evaluateexpression(root.left)
            right = self.evaluateexpression(root.right)

            if root.oper.token_t == TokenType.plus:
                return left + right
            elif root.oper.token_t == TokenType.minus:
                return left - right
            elif root.oper.token_t == TokenType.multiply:
                return left * right
            elif root.oper.token_t in [TokenType.divide, TokenType.modulo]:
                if left == 0:
                    raise ZeroDivisionError()
                return left / right if root.oper.token_t == TokenType.divide else left % right
            elif root.oper.token_t == TokenType.exponent:
                return left ** right
            else:
                raise Exception('Unknown binary operator <{root.oper.token_t.name}>')
        elif isinstance(root, ParenthesizedExpression): # evaluate the expression inside the brackets
            return self.evaluateexpression(root.expr)
        else:
            raise Exception('Unknown node [{root.nType}]')