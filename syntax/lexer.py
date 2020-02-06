from .tokens import * # contains Token, TokenType
from .helper import Helper
import sys
sys.path.append('..')
from textspan import *

class Lexer:
    def __init__(self, input: str):
        self.input = input
        self.pos = 0
        self.helper = Helper()
        self.Diagnostics = Diagnostics()
    
    def current(self) -> chr:
        return self.lookahead(0)
    
    def lookahead(self, offset: int) -> chr:
        # lexing complete condition
        pos = offset + self.pos 
        if pos >= len(self.input):
            return '\0'
        return self.input[pos]

    def next(self):
        # advance current input position by 1
        self.pos += 1
        
    def lex(self) -> Token:
        # number, parenthesis, operators, whitespace
        
        if self.pos+1 > len(self.input):
            return Token(TokenType.eof, self.pos)
        
        if(str.isalpha(self.current())):
            # compute the range of the identifier [alphabets only]
            strt = self.pos
            
            while(str.isalpha(self.current())):
                self.next()

            sbstr = self.input[strt:self.pos]
            # check if the substring is a reserved operator in word form (or, and, not)
            if self.helper.iswordoperator(sbstr):
                ttype = self.helper.getoperatortokentype(sbstr)
                token = Token(ttype, self.pos, sbstr)
            elif self.helper.iskeyword(sbstr):
                token = self.helper.getkeywordtoken(sbstr, strt)
            else:
                self.Diagnostics.report(TextSpan(strt, self.pos-strt), f'ERROR: Unknown identifier [{sbstr}]')
                token = Token(TokenType.bad_token, strt, sbstr)
            return token


        if(str.isdigit(self.current())):
            # compute the range occupied by digits
            strt = self.pos
            
            while(str.isdigit(self.current())):
                self.next()

            sbstr = self.input[strt:self.pos]
            
            # if the entire string of digits cannot be represented as a number, we want to raise an error
            try:
                sbstr = int(sbstr)
            except ValueError:
                self.Diagnostics.reportinvalidnumber(TextSpan(strt, self.pos-strt),sbstr, int)

            token = Token(TokenType.number, strt, sbstr)
            return token

        elif str.isspace(self.current()):
            # for spaces, we want to skip over them, so we apply method similar to 'number'. 
            # But these could be included in the parse tree.
            strt = self.pos
            
            while(str.isspace(self.current())):
                self.next()
            token = Token(TokenType.space, strt)
            return token

        elif self.helper.isoperator(self.current()):
            # checking for operators
            tokentype = self.helper.getoperatortokentype(self.current())
            if tokentype in (TokenType.ampersand, TokenType.pipe):
                if self.lookahead(1) == '|':
                    token = Token(tokentype, self.pos, '||')
                    self.pos += 2
                    return token
                elif self.lookahead(1) == '&':
                    token = Token(tokentype, self.pos, '&&')
                    self.pos += 2
                    return token
            elif tokentype is TokenType.bang:
                if self.lookahead(1) == '=':
                    token = Token(TokenType.notequal, self.pos, '!=')
                    self.pos += 2
                    return token
                else:
                    token = Token(TokenType.bang, self.pos, '!')
                    self.next()
                    return token
            elif tokentype is TokenType.assignment:
                if self.lookahead(1) == '=':
                    token = Token(TokenType.equal, self.pos, '==')
                    self.pos += 2
                    return token
                else:
                    token = Token(TokenType.assignment, self.pos, '=')
                    self.next()
                    return token
            else:
                token = Token(tokentype, self.pos, self.current())
                self.next()
                return token

        elif self.helper.isparenthesis(self.current()):
            # checking for parenthesis
            cur = self.current()
            paren_type = TokenType.open_paren if cur == '(' else TokenType.closed_paren
            token = Token(paren_type, self.pos, cur)
            self.next()
            return token
          
        elif self.current() != '\0':
            # this should handle all unhandled cases and returns a bad token
            self.Diagnostics.report(TextSpan(strt, self.pos-strt), f'Bad character entered [{self.current()}]')
            token = Token(TokenType.bad_token, self.pos, self.current())
            return token