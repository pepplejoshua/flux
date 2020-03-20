from textspan import TextSpan
from syntax.tokentype import TokenType

class Diagnostic:
    def __init__(self, span: TextSpan, msg: str):
        self.textspan = span
        self.message = msg

    def tostring(self) -> str:
        return f"{self.textspan.start}:{self.textspan.end} >> {self.message}"
        
class DiagnosticsBag:
    def __init__(self):
        self.information = []

    def report(self, textspan: TextSpan, msg: str):
        self.information.append(Diagnostic(textspan, msg))
    
    def reportinvalidnumber(self, textspan: TextSpan, text: str, rtype: type):
        msg = f"The number {text} isn't a valid {rtype}."
        self.report(textspan, msg)
    
    def reportbadcharacter(self, pos: int, char: chr):
        msg = f"Bad character input: {char}"
        self.report(TextSpan(pos, 1), msg)
        
    def reportunexpectedtoken(self, span: TextSpan, actual: TokenType, expected: TokenType):
        msg = f'Unexpected token <{actual}>. Expected <{expected}>'
        self.report(span, msg)

    def reportundefinedunaryoperator(self, span: TextSpan, op_text: str, opernd_type: type):
        msg = f"Unary operator {op_text} not defined for type {opernd_type}."
        self.report(span, msg)

    def reportundefinedbinaryoperator(self, span: TextSpan, op_text: str, ltype: type, rtype: type):
        msg = f"Binary operator {op_text} not defined for types {ltype} and {rtype}."
        self.report(span, msg)

    def append(self, diags):
        self.information += diags.information