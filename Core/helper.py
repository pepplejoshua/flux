from Core.tokentype import TokenType
from Core.tokens import Token

# TODO: make all class methods either static or instance methods.
class TokenTypeHelper:
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

    reserved = { TokenType.plus: '+',
                TokenType.minus: '-',
                TokenType.multiply: '*', 
                TokenType.divide: '/', 
                TokenType.assignment: '=',
                TokenType.equal: '==',
                TokenType.modulo: '%',
                TokenType.exponent: '^',
                TokenType.log_or: ('||', 'or'),
                TokenType.log_and: ('&&', 'and'),
                TokenType.log_not: '!',
                TokenType.notequal: '!=',
                TokenType.open_paren: '(',
                TokenType.closed_paren: ')',
                TokenType.true: 'true',
                TokenType.false: 'false'}

    keywords = {'true': TokenType.true,
    'false': TokenType.false,
    'not': TokenType.log_not,
    'and': TokenType.log_and,
    'or': TokenType.log_or}

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
        return val in ('(', ')')
    
    def getoperatortokentype(self, val: chr) -> TokenType:
        """This takes an operator and returns the appropriate token type"""
        if val in self.operators: return self.operators[val]
        elif val in self.keywords:
            return self.keywords[val]

    # get operator precedence of binary operator token else return 
    def getkeywordtoken(self, val: str, pos: int) -> Token:
        if self.iskeyword(val): 
            token_type = self.keywords[val]
            return Token(token_type, pos, val)
        else: return Token(TokenType.identifier, pos, val)
    
    def getreservedwordtext(self, val: TokenType):
        if val in self.reserved:
            return self.reserved[val]
        return None

    # get operator precedence of binary operator token else return 
    @staticmethod
    def getunaryoperatorprecedence(tokentype: TokenType) -> int:
        operators ={TokenType.plus: 7, 
                TokenType.minus: 7, 
                TokenType.log_not: 7}

        pre = operators[tokentype] if (tokentype in operators) else 0
        return pre

    # get operator precedence of binary operator token else return 
    @staticmethod
    def getbinaryoperatorprecedence(tokentype: TokenType) -> int:
        operators ={TokenType.log_or: 1,
                TokenType.log_and: 2,
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

    def getbinaryoperators(self):
        """Iterates over all posible token types and collects all binary operators."""
        bin_ops = []
        for tt in TokenType:
            if self.getbinaryoperatorprecedence(tt) > 0:
                bin_ops.append(tt)
        return bin_ops 

    def getunaryoperators(self):
        """Iterates over all posible token types and collects all unary operators."""
        un_ops = []
        for tt in TokenType:
            if self.getunaryoperatorprecedence(tt) > 0:
                un_ops.append(tt)
        return un_ops 