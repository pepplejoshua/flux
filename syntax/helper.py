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

    keywords = {'true': TokenType.true,
    'false': TokenType.false}

    def isoperator(self, val: str) -> bool:
        """Check if val is an operator"""
        return val in self.operators
    
    def isparenthesis(self, val: str) -> bool:
        """Check if val is either open or closed parenthesis"""
        return val in ['(', ')']

    def iskeyword(self, val: str) -> bool:
        """Check if val is a reserved language identifier"""
        return val in self.keywords

    def getoperatortoken(self, val: str, pos: int) -> Token:
        """This takes an operator and returns the appropriate token type"""
        token_type = self.operators[val]
        if token_type: return Token(token_type, pos, val)
    
    # get operator precedence of binary operator token else return 
    def getkeywordtoken(self, val: str, pos: int) -> Token:
        token_type = self.keywords[val] if (val in self.keywords) else 0
        val = True if val == 'true' else False
        if token_type: return Token(token_type, pos, val)
        else: return Token(TokenType.identifier, pos, val)
    
    # get operator precedence of binary operator token else return 
    @staticmethod
    def getunaryoperatorprecedence(tokentype: TokenType) -> int:
        operators ={TokenType.plus: 4,
                TokenType.minus: 4}

        pre = operators[tokentype] if (tokentype in operators) else 0
        return pre

    # get operator precedence of binary operator token else return 
    @staticmethod
    def getbinaryoperatorprecedence(tokentype: TokenType) -> int:
        operators ={TokenType.plus: 1,
                TokenType.minus: 1,
                TokenType.multiply: 2, 
                TokenType.divide: 2, 
                TokenType.modulo: 2,
                TokenType.exponent: 3}

        pre = operators[tokentype] if (tokentype in operators) else 0
        return pre