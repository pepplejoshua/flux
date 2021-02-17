from flux import entry
import pytest
from termcolor import cprint
from colorama import init
init()

def eval(eq):
        res = entry(True, False, test=True, code=eq)
        return res
    
def test_eval(ln, exp, etype):
        if etype == 'int':
                req = int(exp)
        elif etype == 'bool':
                req = False if exp == 'False' else True
        res = eval(ln)
        cprint(f"\n\nCalculation: {ln} ?= {exp}", 'green')
        cprint(f"Result[{res}] == Expected[{req}]", 'yellow')
        assert res == req