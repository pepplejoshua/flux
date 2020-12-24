import sys
sys.path.append('..')
from .boundoperatortypes import BBinaryOperatorType
from syntax.tokentype import *

# overloading an operator operation type is possible using a tuple of all the return types that it can support. 
# this will require a way of allowing the operation to be evaluated or binded later if it matches one of the permitted types
class BBinaryOperator:
    def __init__(self, ttype: TokenType, bop_type: BBinaryOperatorType, left: type, right: type = None, res: type = None):
        self.tokentype = ttype
        self.operatortype = bop_type
        self.left = left
        self.right = right
        self.resulttype = res
        if not res: 
            self.resulttype = left
        if not right:
            self.right = left

    # based on the token type sent in, we send back an already constructed bound operator (Binary)
    # to add to the bound tree
    @staticmethod
    def bind(ttype: TokenType, left: type, right: type):
        operators = [BBinaryOperator(TokenType.plus, BBinaryOperatorType.plus, int), 
                    BBinaryOperator(TokenType.minus, BBinaryOperatorType.minus, int),
                    BBinaryOperator(TokenType.multiply, BBinaryOperatorType.multiply, int),
                    BBinaryOperator(TokenType.divide, BBinaryOperatorType.divide, int),
                    BBinaryOperator(TokenType.modulo, BBinaryOperatorType.modulo, int),
                    BBinaryOperator(TokenType.exponent, BBinaryOperatorType.exponent, int),
                    BBinaryOperator(TokenType.ampersand, BBinaryOperatorType.log_and, bool),
                    BBinaryOperator(TokenType.pipe, BBinaryOperatorType.log_or, bool),
                    BBinaryOperator(TokenType.equal , BBinaryOperatorType.equal, int, int, res=bool),
                    BBinaryOperator(TokenType.notequal , BBinaryOperatorType.notequal, int, int, res=bool),
                    BBinaryOperator(TokenType.equal , BBinaryOperatorType.equal, bool),
                    BBinaryOperator(TokenType.notequal , BBinaryOperatorType.notequal, bool)]
                        
        for i in operators:
            if i.tokentype == ttype and i.left == left and i.right == right:
                return i
        return None