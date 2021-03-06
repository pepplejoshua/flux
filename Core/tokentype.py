from enum import Enum, auto
# number, parenthesis, operators, whitespace, eof, expression types
class TokenType(Enum):
    # special tokens
    eof = auto()
    bad_token = auto()
    space = auto()
    # literal tokens
    number = auto()
    identifier = auto()
    # keywords
    true = auto()
    false = auto()
    # parenthesis
    open_paren = auto()
    closed_paren = auto()
    # operators
    plus = auto()
    minus = auto()
    multiply = auto()
    modulo = auto()
    divide = auto()
    exponent = auto()
    assignment = auto()
    pipe = auto()
    ampersand = auto()
    bang = auto()
    # bool operators
    log_or = auto()
    log_and = auto()
    log_not = auto()
    #complex operators
    notequal = auto() # bang + assignment
    equal = auto() # assignment + assignment
    # expression tokens
    literal_expr = auto()
    name_expr = auto()
    assignment_expr = auto()
    unary_expr = auto()
    bin_expr = auto()
    paren_expr = auto()
    
# TODO: create TokenTypes and implementations for these
# '+=':, 
# '-=':, 
# '*=':, 
# '/=':, 
# '^=':