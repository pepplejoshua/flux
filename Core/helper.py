from Core.tokentype import TokenType
from Core.tokens import Token

class Helper:
    operators = {'+': TokenType.plus,
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
    'false': TokenType.false,
    'not': TokenType.bang,
    'and': TokenType.ampersand,
    'or': TokenType.pipe}

    def isoperator(self, val: str) -> bool:
        """Check if val is an operator"""
        return val in self.operators
    
    def iskeyword(self, val: str) -> bool:
        return val in self.keywords

    def isKeywordTokenType(self, val: TokenType) -> bool:
        vals = list(self.keywords.values())
        return val in vals


    def isparenthesis(self, val: str) -> bool:
        """Check if val is either open or closed parenthesis"""
        return val in ['(', ')']
    
    def getoperatortokentype(self, val: chr) -> TokenType:
        """This takes an operator and returns the appropriate token type"""
        if val in self.operators: return self.operators[val]
        elif val in self.wordoperators:
            return self.wordoperators[val]

    # get operator precedence of binary operator token else return 
    def getkeywordtoken(self, val: str, pos: int) -> Token:
        if self.iskeyword(val): 
            token_type = self.keywords[val]
            return Token(token_type, pos, val)
        else: return Token(TokenType.identifier, pos, val)
    
    # get operator precedence of binary operator token else return 
    @staticmethod
    def getunaryoperatorprecedence(tokentype: TokenType) -> int:
        operators ={TokenType.plus: 7, 
                TokenType.minus: 7, 
                TokenType.bang: 7}

        pre = operators[tokentype] if (tokentype in operators) else 0
        return pre

    # get operator precedence of binary operator token else return 
    @staticmethod
    def getbinaryoperatorprecedence(tokentype: TokenType) -> int:
        operators ={TokenType.pipe: 1,
                TokenType.ampersand: 2,
                TokenType.equal: 3,
                TokenType.notequal: 3,
                TokenType.plus: 4,
                TokenType.minus: 4,
                TokenType.multiply: 5, 
                TokenType.divide: 5, 
                TokenType.modulo: 5,
                TokenType.exponent: 6}

        pre = operators[tokentype] if (tokentype in operators) else 0
        return pre