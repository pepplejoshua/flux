from .lexer import Lexer
from termcolor import cprint
from .helper import Helper
from .expression import *
import sys
sys.path.append('..')
from textspan import *

# a recursive descent parser (idk what that means atm)
class Parser: 
    def __init__(self, input: str):
        self.exit = False
        self.error = False
        self.pos = 0
        lexer = Lexer(input)
        self.tokens = []
        self.Diagnostics = Diagnostics()
        token = lexer.lex()
        
        # continue to tokenize input until eof is seen, the repl has received an exit command or a bad_token is read
        while token.tokentype.name != 'eof':
            if (token.tokentype not in [TokenType.bad_token, TokenType.space]):
                self.tokens.append(token)
            elif token.tokentype is TokenType.bad_token:
                self.error = True
                break
            token = lexer.lex()
        if self.error:
            self.Diagnostics.append(lexer.Diagnostics)
            return
        elif token.tokentype.name == 'eof': self.tokens.append(token)

    def lookahead(self, offset: int) -> Token:
        # this returns the token offset positions away from current from the list of tokens
        index = offset + self.pos
        if index >= len(self.tokens):
            # if the requested index is beyond the number of tokens, index becomes the last possible index
            index = len(self.tokens) - 1
        return self.tokens[index]

    def current(self) -> Token:
        return self.lookahead(0)

    # this returns the current token after increasing tokens[index] by 1
    def nexttoken(self) -> Token:
        cur = self.current()
        self.pos += 1
        return cur

    # this checks if the current() token is the expected token_type and returns the current token if it is
    # else it returns a fabricated token
    def match(self, token_type: TokenType) -> Token:
        if self.error:
            return Token(token_type, self.current().pos)
        else:
            if (self.current().tokentype == token_type):
                return self.nexttoken()
            else:
                # tell user about unexpected token and what token was expected in that position
                self.Diagnostics.report(self.current.span(), f'ERROR: Unexpected token <{self.current().tokentype}>. Expected <{token_type}>')
                self.error = True
                return Token(token_type, self.current().pos)

    # parsing should begin in the leaves since they're usually the primary expressions
    # like numbers and basic literals
    def parse(self) -> SyntaxTree:
        # this is the main call. 
        expr = self.parseexpression()
        eof_token = self.match(TokenType.eof)
        return SyntaxTree(self.Diagnostics, expr, eof_token)

    # this parses the tree by assuming (TODO: rethink and rewrite):
    # token 1 & 3 = operand
    # token 2 is sent to a function to determine its precedence and perform 
    # a continuous forward look provided a non operator isn't read 
    # or a lower precedence operator isn't read
    def parseexpression(self, parentprecendece=0) -> Expression:
        left: Expression
        un_pre = Helper.getunaryoperatorprecedence(self.current().nodetype())

        # using >= vs > allows you to stack - or + as many times as you wish due to respecting precedence of the same level 
        # --1 would be read as un_op - un_op - literal - number (correctly when using >= since 2 -s appear together)
        # --1 would've been read as un_op - <break since - and - have same precedence> - continue to parseprimaryexpression instead (generates error when in match())
        if un_pre != 0 and un_pre >= parentprecendece:
            sign = self.nexttoken()
            operand = self.parseexpression(un_pre)
            left = UnaryExpression(sign, operand)
        else:
            left = self.parseprimaryexpression()
        # you can choose to handle post-fix cases in between unary ops and regular ops
        while True:
            precedence = Helper.getbinaryoperatorprecedence(self.current().nodetype())
            if precedence == 0 or precedence <= parentprecendece:
                break
            operator = self.nexttoken()
            right = self.parseexpression(precedence)
            left = BinaryExpression(left, operator, right)
        return left
    
    # this will handle number expressions and parenthesized expressions constructions 
    # as they are to be considered first before other expression kinds
    def parseprimaryexpression(self) -> Expression:
        if (self.current().tokentype == TokenType.open_paren):
            left = self.nexttoken()
            expr = self.parseexpression() # entry point to begin parsing
            right = self.match(TokenType.closed_paren)
            return ParenthesizedExpression(left, expr, right)

        elif self.current().tokentype in (TokenType.true, TokenType.false):
            keyword = self.current()
            val = True if self.nexttoken().tokentype == TokenType.true else False # t is t and f otherwise
            val = bool(val)
            return LiteralExpression(keyword, val) 

        else:
            literal_token = self.match(TokenType.number)
            return LiteralExpression(literal_token)