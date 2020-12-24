from textspan import TextSpan
<<<<<<< HEAD
=======
from syntax.tokentype import TokenType
>>>>>>> c8712e7da967f336c28cd1698865615c7e3a890c

class Diagnostic:
    def __init__(self, span: TextSpan, msg: str):
        self.textspan = span
        self.message = msg

    def tostring(self) -> str:
<<<<<<< HEAD
        return f"{self.textspan.start+1}:{self.textspan.end+1} ~> {self.message}"
        
class DiagnosticBag:
    from syntax.tokentype import TokenType

    def __init__(self):
        self.Diagnostics = []

    def report(self, textspan: TextSpan, msg: str):
        self.Diagnostics.append(Diagnostic(textspan, msg))
    
    def reportinvalidnumber(self, textspan: TextSpan, text: str, rtype: type):
        msg = f"The number {text} isn't a valid {rtype.__name__}."
        self.report(textspan, msg)
    
    def reportbadcharacter(self, pos: int, char: chr):
        msg = f"Bad character entered: '{char}'"
        self.report(TextSpan(pos, 1), msg)

    def reportunexpectedtoken(self, tokenspan: TextSpan, tokentype: TokenType, exp_tokentype: TokenType):
        msg = f"Unexpected token <{tokentype}>, expected <{exp_tokentype}>"
        self.report(tokenspan, msg)

    def reportundefinedunaryoperator(self, tokenspan: TextSpan, tokensign: str, operandtype):
        msg = f"Unary operator '{tokensign}' not defined for type {operandtype.__name__}."
        self.report(tokenspan, msg)
        
    def reportundefinedbinaryoperator(self, operspan: TextSpan, tokensign: str, ltype, rtype):
        msg = f"Binary operator '{tokensign}' not defined for types {ltype.__name__} and {rtype.__name__}."
        self.report(operspan, msg)
        
    def append(self, diags):
        self.Diagnostics += diags.Diagnostics
=======
        return f"{self.spantostring()} -> {self.errortostring()}"
    
    def spantostring(self) -> str:
        return f"{self.textspan.start+1}:{self.textspan.end}"

    def errortostring(self) -> str:
        return f"{self.message}"

class DiagnosticsBag:
    def __init__(self):
        self.information = []

    def report(self, textspan: TextSpan, msg: str):
        self.information.append(Diagnostic(textspan, msg))
    
    def reportinvalidnumber(self, textspan: TextSpan, text: str, rtype: type):
        msg = f"The number '{text}' isn't a valid {rtype}."
        self.report(textspan, msg)
    
    def reportbadcharacter(self, pos: int, char: chr):
        msg = f"Bad character input: '{char}'"
        self.report(TextSpan(pos, 1), msg)
        
    def reportunexpectedtoken(self, span: TextSpan, actual: TokenType, expected: TokenType):
        msg = f'Unexpected token <{actual}>. Expected <{expected}>'
        self.report(span, msg)

    def reportundefinedunaryoperator(self, span: TextSpan, op_text: str, opernd_type: type):
        msg = f"Unary operator '{op_text}' not defined for type {opernd_type}."
        self.report(span, msg)

    def reportunknownidentifier(self, span: TextSpan, iden: str):
        msg = f"Unknown identifier '{iden}'"
        self.report(span, msg)

    def reportundefinedbinaryoperator(self, span: TextSpan, op_text: str, ltype: type, rtype: type):
        msg = f"Binary operator '{op_text}' not defined for types {ltype} and {rtype}."
        self.report(span, msg)

    def append(self, diags):
        self.information += diags.information
>>>>>>> c8712e7da967f336c28cd1698865615c7e3a890c
