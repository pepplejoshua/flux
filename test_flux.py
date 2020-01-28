from flux import entry
import pytest
import sys
from termcolor import cprint

def eval(eq):
        res = entry(True, False, test=True, code=eq)
        return res
    
def test_eval(ln, exp, etype):
        if etype == 'int':
                req = int(exp)
        elif etype == 'bool':
                req = False if exp == 'false' else True
        cprint(f"\n\nCalculation: {ln} ?= {exp}", 'green')
        cprint(f"Result[{res}] == Expected[{req}]", 'yellow')
        assert res == req