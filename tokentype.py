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
    # parenthesis
    open_paren = auto()
    closed_paren = auto()
    # operators
    plus = auto()
    minus = auto()
    multiply = auto()
    divide = auto()
    modulo = auto()
    exponent = auto()
    assignment = auto()
    # expression tokens
    literal_expr = auto()
    unary_expr = auto()
    bin_expr = auto()
    paren_expr = auto()
    
# TODO: create TokenTypes and implementations for these
# '+=':, 
# '-=':, 
# '*=':, 
# '/=':, 
# '^=':