from tokentype import TokenType
from token import Token
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
    def isoperator(self, val):
        """Check if val is an operator"""
        return val in self.operators
    
    def isparenthesis(self, val):
        """Check if val is either open or closed parenthesis"""
        return val in ['(', ')']

    def isidentifier(self, val):
        """Check if val is a reserved language identifier"""
        return val in self.ident

    def getoperatortokentype(self, val, pos):
        """This takes an operator and returns the appropriate token type"""
        token_type = self.operators[val]
        if token_type: return Token(token_type, pos, val)