from flux import entry
import pytest
import sys

print(sys.argv)
def eval(eq):
        res = entry(True, False, test=True, code=eq)
        return res
    
def test_eval(ln, exp):
        req = int(exp)
        res = eval(ln)
        print(res, '==', req)
        assert res == req
