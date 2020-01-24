from .tokentype import TokenType
from .tokens import Token
from termcolor import cprint
class Helper:
    operators ={'+': TokenType.plus,
                '-': TokenType.minus,
                '*': TokenType.multiply, 
                '/': TokenType.divide, 
                '=': TokenType.assignment, 
                '%': TokenType.modulo,
                '^': TokenType.exponent}
    ident = []
    def isoperator(self, val: str):
        """Check if val is an operator"""
        return val in self.operators
    
    def isparenthesis(self, val: str):
        """Check if val is either open or closed parenthesis"""
        return val in ['(', ')']

    def isidentifier(self, val: str):
        """Check if val is a reserved language identifier"""
        return val in self.ident

    def getoperatortoken(self, val: str, pos: int):
        """This takes an operator and returns the appropriate token type"""
        token_type = self.operators[val]
        if token_type: return Token(token_type, pos, val)
    
    # get operator precedence of binary operator token else return 
    @staticmethod
    def getunaryoperatorprecedence(tokentype: TokenType):
        operators ={TokenType.plus: 4,
                TokenType.minus: 4}

        pre = operators[tokentype] if (tokentype in operators) else 0
        return pre
    
    # get operator precedence of binary operator token else return 
    @staticmethod
    def getbinaryoperatorprecedence(tokentype: TokenType):
        operators ={TokenType.plus: 1,
                TokenType.minus: 1,
                TokenType.multiply: 2, 
                TokenType.divide: 2, 
                TokenType.modulo: 2,
                TokenType.exponent: 3}

        pre = operators[tokentype] if (tokentype in operators) else 0
        return pre
