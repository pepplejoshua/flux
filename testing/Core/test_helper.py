from .fixtures import tokenTypeEnumItems, lexer, \
    assertNumberEq, assertEOF, assertTextEq, assertTokenTypesEq
from Core import TokenType, Helper

runTestsCounter = 0

# helpers
def testReservedWordText(tokenTypeEnumItems, lexer):
    def inner(tt: TokenType):
        text = Helper().getreservedwordtext(tt)
        # for things like expression types, eof and spaces, as we only want reserved words and characters 
        if not text: 
            return
        # for the pipe and ampersand cases (logical or and and),
        # I account for there being 2 different ways to enter it into the program
        def performAssertions(text):
            toks = lexer(text)
            assertNumberEq(2, len(toks))
            tok = toks[0]
            end = toks[1]
            assertEOF(end)
            assertTokenTypesEq(tok, tt)
            assertTextEq(tok, text)
            global runTestsCounter
            runTestsCounter += 1
        if type(text) is tuple:
            for t in text:
                performAssertions(t)
        else:
            performAssertions(text)
   
    for tt in tokenTypeEnumItems:
        try:
            inner(tt)
        except AssertionError as e:
            print(e)
            print("Found On", tt)

def testShowTestCount():
    global runTestsCounter
    print('\n', runTestsCounter, "tests completed in", __file__)