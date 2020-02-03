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
                '^': TokenType.exponent,
                '|': TokenType.pipe,
                '&': TokenType.ampersand, 
                '!': TokenType.bang}

    keywords = {'true': TokenType.true,
    'false': TokenType.false}
    
    wordoperators = {
        'not': TokenType.bang,
        'and': TokenType.ampersand,
        'or': TokenType.pipe
    }

    def isoperator(self, val: str) -> bool:
        """Check if val is an operator"""
        return val in self.operators
    
    def isparenthesis(self, val: str) -> bool:
        """Check if val is either open or closed parenthesis"""
        return val in ['(', ')']

    def iswordoperator(self, val: str) -> bool:
        return val in self.wordoperators

    def iskeyword(self, val: str) -> bool:
        """Check if val is a reserved language identifier"""
        return val in self.keywords
    
    def getoperatortokentype(self, val: chr) -> TokenType:
        """This takes an operator and returns the appropriate token type"""
        if val in self.operators: return self.operators[val]
        elif val in self.wordoperators:
            return self.wordoperators[val]

    # get operator precedence of binary operator token else return 
    def getkeywordtoken(self, val: str, pos: int) -> Token:
        token_type = self.keywords[val] if (val in self.keywords) else 0
        val = True if val == 'true' else False
        if token_type: return Token(token_type, pos, val)
        else: return Token(TokenType.identifier, pos, val)
    
    # get operator precedence of binary operator token else return 
    @staticmethod
    def getunaryoperatorprecedence(tokentype: TokenType) -> int:
        operators ={TokenType.plus: 6,
                TokenType.minus: 6, 
                TokenType.bang: 6}

        pre = operators[tokentype] if (tokentype in operators) else 0
        return pre

    # get operator precedence of binary operator token else return 
    @staticmethod
    def getbinaryoperatorprecedence(tokentype: TokenType) -> int:
        operators ={TokenType.pipe: 1,
                TokenType.ampersand: 2,
                TokenType.plus: 3,
                TokenType.minus: 3,
                TokenType.multiply: 4, 
                TokenType.divide: 4, 
                TokenType.modulo: 4,
                TokenType.exponent: 5}

        pre = operators[tokentype] if (tokentype in operators) else 0
        return pre