from lexer import Lexer
from termcolor import cprint
from expression import *
# a recursive descent parser (idk what that means atm)
class Parser: 
    def __init__(self, input):
        self.exit = False
        self.error = False
        self.pos = 0
        lexer = Lexer(input)
        self.tokens = []
        self.diagnostics = []
        token = lexer.lex()
        
        # continue to tokenize input until eof is seen, the repl has received an exit command or a bad_token is read
        while token.token_t.name != 'eof':
            if (token.token_t not in [TokenType.bad_token, TokenType.space]):
                self.tokens.append(token)
            elif token.token_t is TokenType.bad_token:
                self.error = True
                break
            token = lexer.lex()
        if self.error:
            self.diagnostics += lexer.diagnostics
            return
        elif token.token_t.name == 'eof': self.tokens.append(token)

    def lookahead(self, offset):
        # this returns the token offset positions away from current from the list of tokens
        index = offset + self.pos
        if index >= len(self.tokens):
            # if the requested index is beyond the number of tokens, index becomes the last possible index
            index = len(self.tokens) - 1
        return self.tokens[index]

    def current(self):
        return self.lookahead(0)

    # this returns the current token after increasing tokens[index] by 1
    def nexttoken(self):
        cur = self.current()
        self.pos += 1
        return cur

    # this checks if the current() token is the expected token_type and returns the current token if it is
    # else it returns a fabricated token
    def match(self, token_type):
        if self.error:
            return Token(token_type, self.current().pos)
        else:
            if (self.current().token_t == token_type):
                return self.nexttoken()
            else:
                # tell user about unexpected token and what token was expected in that position
                self.diagnostics.append(f'ERROR: Unexpected token <{self.current().token_t}>. Expected <{token_type}>')
                self.error = True
                return Token(token_type, self.current().pos)

    # parsing should begin in the leaves since they're usually the primary expressions
    # like numbers and basic literals
    def parse(self):
        # this is the main call. 
        expr = self.parseexpression()
        eof_token = self.match(TokenType.eof)
        return SyntaxTree(self.diagnostics, expr, eof_token)

    # this parses the tree by assuming:
    # token 1 & 3 = operand
    # token 2 is sent to a function to determine its precedence and perform 
    # a continuous forward look provided a non operator isn't read 
    # or a lower precedence operator isn't read
    def parseexpression(self, parentprecendece=0):
        left = self.parseprimaryexpression()

        while True:
            precedence = self.getbinaryoperatorprecedence(self.current().nType())
            if precedence == 0 or precedence <= parentprecendece:
                break
            operator = self.nexttoken()
            right = self.parseexpression(precedence)
            left = BinaryExpression(left, operator, right)
        return left
    
    # get operator precedence of binary operator token else return 0
    def getbinaryoperatorprecedence(self, tokentype):
        operators ={TokenType.plus: 1,
                TokenType.minus: 1,
                TokenType.multiply: 2, 
                TokenType.divide: 2, 
                TokenType.modulo: 2,
                TokenType.exponent: 3}


        pre = operators[tokentype] if tokentype in operators else 0
        return pre

    # this will handle number expressions and parenthesized expressions constructions 
    # as they are to be considered first before other expression kinds
    def parseprimaryexpression(self):
        if (self.current().token_t == TokenType.open_paren):
            left = self.nexttoken()
            expr = self.parseexpression() # entry point to begin parsing
            right = self.match(TokenType.closed_paren)
            return ParenthesizedExpression(left, expr, right)

        literal_token = self.match(TokenType.number)
        return LiteralExpression(literal_token)