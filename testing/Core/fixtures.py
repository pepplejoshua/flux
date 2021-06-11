import pytest
from Core import SyntaxTree, TokenType, Helper

sc = "module"

# defines a lexer fixture that returns a function
# that does the actual lexing work. Used for redirecting "line"
@pytest.fixture(scope=sc)
def lexer():
    def makeLexer(line: str):
        return SyntaxTree.lexTokens(line)
    return makeLexer

# defines a tokens fixture that returns an array of 2 tuples
# containing a TokenType and some text to match it
@pytest.fixture(scope=sc)
def tokens():
    toks = [
        (TokenType.identifier, 'a'),
        (TokenType.identifier, 'someVariable'),

        (TokenType.number, '54321'),
        (TokenType.number, '0'),

        (TokenType.true, 'true'),
        (TokenType.false, 'false'),

        (TokenType.open_paren, '('),
        (TokenType.closed_paren, ')'),

        (TokenType.plus, '+'),
        (TokenType.minus, '-'),
        (TokenType.multiply, '*'),
        (TokenType.divide, '/'),
        (TokenType.modulo, '%'),
        (TokenType.exponent, '^'),
        (TokenType.assignment, '='),
        
        (TokenType.pipe, '||'),
        (TokenType.pipe, 'or'),
        (TokenType.ampersand, '&&'),
        (TokenType.ampersand, 'and'),
        (TokenType.bang, '!'),
        (TokenType.bang, 'not'),

        (TokenType.notequal, '!='),
        (TokenType.equal, '=='),
    ]
    return toks

@pytest.fixture(scope=sc)
def spaceTokens():
    toks = [
        (TokenType.space, ' '),
        (TokenType.space, '     '),
        (TokenType.space, '\t'),
        (TokenType.space, '\n'),
        (TokenType.space, '\r'),
        (TokenType.space, '\r\n'),
        (TokenType.space, '\t\n'),
    ]
    return toks

@pytest.fixture(scope=sc)
def tokenPairs(tokens):
    toks = []
    for t1 in tokens:
        for t2 in tokens:
            if not requireSeparator(t1[0], t2[0]):
                toks.append((t1[0], t1[1], t2[0], t2[1]))
    return toks

@pytest.fixture(scope=sc)
def tokenPairsWithSpaces(tokens, spaceTokens):
    toks = []
    for t1 in tokens:
        for t2 in tokens:
            if requireSeparator(t1[0], t2[0]):
                for sp in spaceTokens:
                    toks.append((t1[0], t1[1], sp[0], sp[1], t2[0], t2[1]))
    return toks

# helper func to identify token pairs requiring spaces
def requireSeparator(a: TokenType, b: TokenType) -> bool:
    if (a == TokenType.identifier and b == TokenType.identifier):
        return True
    
    aIsKeyword = Helper().isKeywordTokenType(a)
    bIsKeyword = Helper().isKeywordTokenType(b)
    if (aIsKeyword and bIsKeyword):
        return True
    if (aIsKeyword and b == TokenType.identifier):
        return True
    if (a == TokenType.identifier and bIsKeyword):
        return True

    
    if (a == TokenType.number and b == TokenType.number):
        return True
    

    if (a == TokenType.bang and b == TokenType.assignment):
        return True 
    if (a == TokenType.bang and b == TokenType.equal):
        return True    


    if (a == TokenType.assignment and b == TokenType.assignment):
        return True    
    if (a == TokenType.equal and b == TokenType.assignment):
        return True    
    if (a == TokenType.assignment and b == TokenType.equal):
        return True    
    if (a == TokenType.equal and b == TokenType.equal):
        return True    

    
    return False
