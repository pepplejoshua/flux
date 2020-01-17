from token import * # contains Token, TokenType
from helper import Helper
class Lexer:
    def __init__(self, input):
        self.input = input
        self.pos = 0
        self.helper = Helper()
        self.diagnostics = []
    
    def current(self):
        # lexing complete condition
        if self.pos >= len(self.input):
            return '\0'
        return self.input[self.pos]

    def next(self):
        # advance current input position by 1
        self.pos += 1
        
    def nextToken(self):
        # number, parenthesis, operators, whitespace
        
        if self.pos+1 > len(self.input):
            return Token(TokenType.eof, self.pos)
        
        if(str.isalpha(self.current())):
            # compute the range of the identifier [alphabets only]
            strt = self.pos
            
            while(str.isalpha(self.current())):
                self.next()

            sbstr = self.input[strt:self.pos]
            # check if the substring is a reserved identifier
            if self.helper.isidentifier(sbstr):
                token = Token(TokenType.identifier, strt, sbstr)
            else:
                self.diagnostics.append(f'ERROR: Unknown identifier [{sbstr}]')
                token = Token(TokenType.bad_token, strt, sbstr)
            return token


        if(str.isdigit(self.current())):
            # compute the range occupied by digits
            strt = self.pos
            
            while(str.isdigit(self.current())):
                self.next()

            sbstr = self.input[strt:self.pos]
            sbstr = int(sbstr)
            
            # if the entire string of digits cannot be represented as a number, we want to raise an error
            if not sbstr:
                self.diagnostics.append(f'ERROR: [{sbstr}] isn\'t a valid number')

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
            token = self.helper.getoperatortokentype(self.current(), self.pos)
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
            self.diagnostics.append(f'Bad character entered [{self.current()}]')
            token = Token(TokenType.bad_token, self.pos, self.current())
            return token