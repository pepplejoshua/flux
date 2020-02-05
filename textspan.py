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
        return self.message
        