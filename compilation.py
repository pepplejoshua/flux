from binding.binder import Binder
from syntax.syntax import SyntaxTree
from evaluator import BExpressionEvaluator
from diagnostics import DiagnosticsBag
class Compilation:
    def __init__(self, tree: SyntaxTree):
        self.tree = tree
    
    def evaluate(self):
        if self.tree.error:
            diag = self.tree.diagnostics.information
            return EvaluationResult(None, diag, None)
        binder = Binder()
        b_expr = binder.bindexpression(self.tree.root)
<<<<<<< HEAD
        self.tree.Diagnostics.append(binder.Diagnostics)
        diag = self.tree.Diagnostics.Diagnostics
=======
        diag = self.tree.diagnostics.information + binder.diagnostics.information
>>>>>>> c8712e7da967f336c28cd1698865615c7e3a890c
        eval = BExpressionEvaluator(b_expr)
        res = eval.evaluate()
        if diag: return EvaluationResult(None, diag, None)
        return EvaluationResult(b_expr, [], res)

class EvaluationResult:
    def __init__(self, boundExpr, diag: [], value):
        self.boundExpr = boundExpr
        self.value = value
        self.Diagnostics = diag