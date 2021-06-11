from .fixtures import lexer, tokens, tokenPairs, spaceTokens, tokenPairsWithSpaces
from Core import TokenType, Token, tokentype

runTestsCounter = 0

def assertEOF(t: Token):
    assertEQTokenTypes(t, TokenType.eof)

def assertEQTokenTypes(t1: Token, tt: TokenType):
    assert t1.tokentype == tt

def assertEQLines(t1: Token, line: str):
    assert str(t1.val) == line


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
        assertEQTokenTypes(tok, tokType)
        # check for equal token values
        assertEQLines(tok, tokLine)
    # this allows me to append in the space tokens 
    # so other tokens can be reused later in pair testing
    tks = tokens + spaceTokens
    global runTestsCounter 
    tCounter = 0
    for tt, txt in tks:
        inner(tt, txt)
        tCounter += 1
    print('\n', tCounter, "tests completed")
    runTestsCounter += tCounter

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
        assertEQTokenTypes(tok1, ttype1)
        assertEQLines(tok1, tLine1)
        assertEQTokenTypes(tok2, ttype2)
        assertEQLines(tok2, tLine2)

    global runTestsCounter
    tCounter = 0
    for bundle in tokenPairs:
        inner(*bundle)
        tCounter += 1
    print('\n', tCounter, "tests completed")
    runTestsCounter += tCounter

def testPairedTokensWithSeparators(lexer, tokenPairsWithSpaces):
    def inner(ttype1: TokenType, lne1: str, separatorTtype: TokenType, sepText: str, ttype2: TokenType, lne2: str):
        txt = lne1+sepText+lne2
        toks = lexer(txt)

        assert 4 == len(toks)

        tok1 = toks[0]
        tok2 = toks[1]
        tok3 = toks[2]
        end = toks[3]
        assertEOF(end)
        assertEQTokenTypes(tok1, ttype1)
        assertEQLines(tok1, lne1)
        assertEQTokenTypes(tok2, separatorTtype)
        assertEQLines(tok2, sepText)
        assertEQTokenTypes(tok3, ttype2)
        assertEQLines(tok3, lne2)

    global runTestsCounter
    tCounter = 0
    for bundle in tokenPairsWithSpaces:
        inner(*bundle)
        tCounter += 1
    print('\n', tCounter, "tests completed")
    runTestsCounter += tCounter


def testShowTestCount():
    global runTestsCounter
    print('\n', runTestsCounter, "tests completed")