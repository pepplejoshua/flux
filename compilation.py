from binding.binder import Binder
from Core.syntax import SyntaxTree
from evaluator import BExpressionEvaluator
class Compilation:
    def __init__(self, tree: SyntaxTree):
        self.tree = tree
    
    def evaluate(self, variables):
        binder = Binder(variables)
        b_expr = binder.bindexpression(self.tree.root)

        diag = binder.diagnostics.information

        if diag: return EvaluationResult(None, diag, None)
        eval = BExpressionEvaluator(b_expr, variables)
        res = eval.evaluate()
        return EvaluationResult(b_expr, [], res)

class EvaluationResult:
    def __init__(self, boundExpr, diag, value):
        self.boundExpr = boundExpr
        self.value = value
        self.diagnostics = diag