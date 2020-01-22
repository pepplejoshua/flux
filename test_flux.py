from flux import entry
import pytest
import sys
from termcolor import cprint

def eval(eq):
        res = entry(True, False, test=True, code=eq)
        return res
    
def test_eval(ln, exp):
        req = int(exp)
        res = eval(ln)
        cprint(f"\n\nCalculation: {ln}", 'green')
        cprint(f"Result[{res}] == Expected[{req}]", 'yellow')
        assert res == req
