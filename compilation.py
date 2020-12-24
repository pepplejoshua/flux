from binding.binder import Binder
from syntax.syntax import SyntaxTree
from evaluator import BExpressionEvaluator

class Compilation:
    def __init__(self, tree: SyntaxTree):
        self.tree = tree
    
    def evaluate(self):
        binder = Binder()
        b_expr = binder.bindexpression(self.tree.root)
        self.tree.Diagnostics.append(binder.Diagnostics)
        diag = self.tree.Diagnostics.Diagnostics
        eval = BExpressionEvaluator(b_expr)
        res = eval.evaluate()
        if diag: return EvaluationResult(diag, None)
        return EvaluationResult([], res)

class EvaluationResult:
    def __init__(self, diag: [], value):
        self.value = value
        self.Diagnostics = diag