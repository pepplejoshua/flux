from .boundoperatortypes import BUnaryOperatorType
from Core.tokentype import *

class BUnaryOperator:
    def __init__(self, ttype: TokenType, uop_type: BUnaryOperatorType, op_type: type, res: type = None):
        self.tokentype = ttype
        self.operatortype = uop_type
        self.operandtype = op_type
        self.resulttype = res
        if not res:
            self.resulttype = op_type

    @staticmethod
    def bind(ttype: TokenType, op_type: type):
        operators = [BUnaryOperator(TokenType.bang, BUnaryOperatorType.log_negate, bool), 
                        BUnaryOperator(TokenType.plus, BUnaryOperatorType.identity, int),
                        BUnaryOperator(TokenType.minus, BUnaryOperatorType.negate, int)]
        for i in operators:
            if i.tokentype == ttype and i.operandtype == op_type:
                return i
        return None
    