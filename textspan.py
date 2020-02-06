class TextSpan:
    def __init__(self, st: int, ln: int):
        self.start = st
        self.length = ln
        self.end = st+ln

class Diagnostic:
    def __init__(self, span: TextSpan, msg: str):
        self.textspan = span
        self.message = msg

    def tostring(self) -> str:
        return f"{self.textspan.start}:{self.textspan.end} >> {self.message}"
        
class Diagnostics:
    def __init__(self):
        self.diagnostics = []

    def report(self, textspan: TextSpan, msg: str):
        self.diagnostics.append(Diagnostic(textspan, msg))
    
    def reportinvalidnumber(self, textspan: TextSpan, text: str, rtype: type):
        msg = f"The number {text} isn't a valid {rtype}."
        self.report(textspan, msg)
    
    def reportbadcharacter(Self, pos: int, char: chr):
        msg = f"Bad character input: {char}"
        self.report(TextSpan(pos, 1), msg)
        
    def append(self, diags):
        self.diagnostics += diags.diagnostics