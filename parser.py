from lexer import Lexer
from termcolor import cprint
from expression import *
# a recursive descent parser (idk what that means atm)
# this means that the parser can be broken down into functions that cover different areas of the grammar
# reducing importance:
# parseexponent() ^ will be the exponent symbol
# parsefactors() *, / and % will be a separate function since they have higher precedence (separate function which gets called first)
# parseterms() +, - will be in the regular precedence level (main parse function)
# since parseterms() is called first and parsefactors() implements the same logic as it,
# calling parsefactors() before any execution inside parseterms() ensures that a higher precedence subtree is built and returned as 
# the operand of a lower precedence subtree
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
            self.diagnostics += lex.diagnostics
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
        expr = self.parseterm()
        eof_token = self.match(TokenType.eof)
        return SyntaxTree(self.diagnostics, expr, eof_token)

    # this is the entry point to begin parsing and building the tree
    # parse regular operators last, due to the order of the calls
    def parseterm(self):
        left = self.parsefactor()
        
        cur = self.current()
        while(cur.token_t == TokenType.plus \
            or cur.token_t == TokenType.minus \
            and not self.error):
            oper = self.nexttoken()
            right = self.parsefactor()
            left = BinaryExpression(left, oper, right)
            cur = self.current()
        return left

    # this makes sure *, / and % are built into the tree second
    def parsefactor(self):
        left = self.parseexponent()
        
        cur = self.current()

        
        # recursive descent works here. why?
        while(cur.token_t == TokenType.multiply \
            or cur.token_t == TokenType.divide \
            or cur.token_t == TokenType.modulo \
            and not self.error):
            oper = self.nexttoken()
            right = self.parseexponent()
            left = BinaryExpression(left, oper, right)
            cur = self.current()
        return left

    # this makes sure exponents are built into the tree first
    def parseexponent(self):
        left = self.parseprimaryexpression()
        
        cur = self.current()

        # recursive descent works here. why?
        while(cur.token_t == TokenType.exponent \
            and not self.error):
            oper = self.nexttoken()
            right = self.parseprimaryexpression()
            left = BinaryExpression(left, oper, right)
            cur = self.current()
        return left


    # this will handle number expressions and parenthesized expressions constructions 
    # as they are to be considered first before other expression kinds
    def parseprimaryexpression(self):
        if (self.current().token_t == TokenType.open_paren):
            left = self.nexttoken()
            expr = self.parseterm() # entry point to begin parsing
            right = self.match(TokenType.closed_paren)
            return ParenthesizedExpression(left, expr, right)

        num_token = self.match(TokenType.number)
        return LiteralExpression(num_token)