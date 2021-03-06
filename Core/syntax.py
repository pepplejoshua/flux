from Core.tokentype import TokenType
from abc import ABC, abstractmethod
from .diagnostics import DiagnosticsBag


# a base node type for syntax tree
class SyntaxNode(ABC):
    @abstractmethod
    def nodetype(_):
        # _ because self is not used
        pass

    @abstractmethod
    def getchildren(_):
        pass

# a syntax tree class which is just a class containing a root to attached ASyntaxNode(s)
class SyntaxTree:
    def __init__(self, diagnostics: DiagnosticsBag, root: SyntaxNode, eof_token, error=False):
        self.diagnostics = diagnostics
        self.root = root
        self.eof = eof_token
        self.error = error

    @staticmethod
    def parse(line: str): 
        from .parser import Parser
        parser = Parser(line)
        return parser.parse()

    @staticmethod
    def lexTokens(line: str):
        from .lexer import Lexer
        lexer = Lexer(line)
        toks = []
        while True:
            tok = lexer.lex()
            toks.append(tok)
            # hoping to catch bad tokens as well
            if tok.tokentype in (TokenType.eof, TokenType.bad_token):
                break
        return toks



# this is my original tree evaluator (unbound tree)
# from syntax.expression import *
# # this recursively traverses a parse tree[SyntaxTree] and returns a result
# class ExpressionEvaluator:
#     def __init__(self, rootExpr: Expression):
#         self.root = rootExpr
    
#     def evaluate(self):
#         return self.evaluateexpression(self.root)

#     def evaluateexpression(self, root):
#         # separate case for separate expression types 
#         # num_expr, bin_expr, unary_expr, paren_expr
        
#         if isinstance(root, LiteralExpression):
#             return root.token.val

#         elif isinstance(root, UnaryExpression):
#             sign = root.sign
#             oper = self.evaluateexpression(root.operand)

#             if sign.tokentype == TokenType.plus:
#                 return oper
#             elif sign.tokentype == TokenType.minus:
#                 return -oper
#             else: raise Exception(f'Unknown unary operator <{root.oper.tokentype.name}>')

#         elif isinstance(root, BinaryExpression):
#             left = self.evaluateexpression(root.left)
#             right = self.evaluateexpression(root.right)

#             if root.oper.tokentype == TokenType.plus:
#                 return left + right
#             elif root.oper.tokentype == TokenType.minus:
#                 return left - right
#             elif root.oper.tokentype == TokenType.multiply:
#                 return left * right
#             elif root.oper.tokentype in [TokenType.divide, TokenType.modulo]:
#                 if left == 0:
#                     raise ZeroDivisionError()
#                 return left / right if root.oper.tokentype == TokenType.divide else left % right
#             elif root.oper.tokentype == TokenType.exponent:
#                 return left ** right
#             else:
#                 raise Exception(f'Unknown binary operator <{root.oper.tokentype.name}>')

#         elif isinstance(root, ParenthesizedExpression): # evaluate the expression inside the brackets
#             return self.evaluateexpression(root.expr)

#         else:
#             raise Exception(f'Unknown node [{root.nodetype()}]')
