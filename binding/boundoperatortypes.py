from enum import Enum, auto

# bound unary operators types
class BUnaryOperatorType(Enum):
    identity = auto()
    negate = auto()
    bool_negate = auto()

# bound binary operators types
class BBinaryOperatorType(Enum):
    plus = auto()
    minus = auto()
    multiply = auto()
    divide = auto()
    modulo = auto()
    exponent = auto()
    assignment = auto() 
    log_and = auto()
    log_or = auto()
    notequal = auto()
    equal = auto()