from .fixtures import lexer, tokens, tokenPairs, spaceTokens
from Core import TokenType, Token, tokentype

c = 0

# called by testTokens to verify inputs with single tokens are tokenized
# properly
def testSingleTokens(lexer, tokens, spaceTokens):
    def inner(tokType: TokenType, tokLine : str):
        toks = lexer(tokLine)

        # since it's a single tokenizable item in tokLine ,
        # toks should be of length 2 (including eof token)
        assert 2 == len(toks)
        tok = toks[0]
        end = toks[1]
        assertEOF(end)

        # check for equal token types
        assetEQTokenTypes(tok, tokType)
        # check for equal token values
        assertEQLines(tok, tokLine)
    # this allows me to append in the space tokens 
    # so other tokens can be reused later in pair testing
    tks = tokens + spaceTokens
    global c
    for tt, txt in tks:
        inner(tt, txt)
        c += 1

def testPairedTokens(lexer, tokenPairs):
    def inner(ttype1: TokenType, tLine1: str, ttype2: TokenType, tLine2: str):
        txt = tLine1 + tLine2
        toks = lexer(txt)

        # since there are 2 tokenizable items in txt,
        # toks should be of length 3 (including eof token)
        assert 3 == len(toks)

        tok1 = toks[0]
        tok2 = toks[1]
        end = toks[2]
        assertEOF(end)

        # make sure the token types generated are as expected
        # and their matching code strings are equal
        assetEQTokenTypes(tok1, ttype1)
        assertEQLines(tok1, tLine1)
        assetEQTokenTypes(tok2, ttype2)
        assertEQLines(tok2, tLine2)

    global c
    for tt1, txt1, tt2, txt2 in tokenPairs:
        inner(tt1, txt1, tt2, txt2)
        c += 1

def assertEOF(t: Token):
    assetEQTokenTypes(t, TokenType.eof)

def assetEQTokenTypes(t1: Token, tt: TokenType):
    assert t1.tokentype == tt

def assertEQLines(t1: Token, line: str):
    assert str(t1.val) == line

def testShowTestCount():
    global c
    print('\n', c, "tests completed")
