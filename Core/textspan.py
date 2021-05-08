class TextSpan:
    def __init__(self, st: int, ln: int):
        self.start = st
        self.length = ln
        self.end = st+ln

        