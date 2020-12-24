from textspan import TextSpan

class Diagnostic:
    def __init__(self, span: TextSpan, msg: str):
        self.textspan = span
        self.message = msg

    def tostring(self) -> str:
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