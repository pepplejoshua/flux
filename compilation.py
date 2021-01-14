from binding.binder import Binder
from syntax.syntax import SyntaxTree
from evaluator import BExpressionEvaluator
class Compilation:
    def __init__(self, tree: SyntaxTree):
        self.tree = tree
    
    def evaluate(self, variables):
        if self.tree.error:
            diag = self.tree.diagnostics.information
            return EvaluationResult(None, diag, None)
        binder = Binder(variables)
        b_expr = binder.bindexpression(self.tree.root)

        self.tree.Diagnostics.append(binder.Diagnostics)
        diag = self.tree.Diagnostics.Diagnostics

        diag = self.tree.diagnostics.information + binder.diagnostics.information
        eval = BExpressionEvaluator(b_expr)
        res = eval.evaluate()

        if diag: return EvaluationResult(None, diag, None)
        eval = BExpressionEvaluator(b_expr, variables)
        res = eval.evaluate()
        return EvaluationResult(b_expr, [], res)

class EvaluationResult:
    def __init__(self, boundExpr, diag, value):
        self.boundExpr = boundExpr
        self.value = value
        self.Diagnostics = diag