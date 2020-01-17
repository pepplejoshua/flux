from enum import Enum, auto
# number, parenthesis, operators, whitespace, eof, expression types
class TokenType(Enum):
    eof = auto()
    # base type
    number = auto()
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
    # special tokens
    space = auto()
    bad_token = auto()
    identifier = auto
    # expression tokens
    num_expr = auto()
    bin_expr = auto()
    paren_expr = auto()
# TODO: create TokenTypes and implementations for these
# '+=':, 
# '-=':, 
# '*=':, 
# '/=':, 
# '^=':