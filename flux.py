from Core.tokens import *
from evaluator import *
from os import system, name
from binding.binder import *
from binding.boundexpression import *
import sys 
from termcolor import cprint
from compilation import *

from colorama import init
init()

def entry(flag, nline, test=False, code=False):
    # get single line and then tokenize repeatedly > repl
    if not test:
        cprint('Flux v0.0.1', 'green')
    res = None
    showtree = False
    history = []
    variables = {}
    while True:
        # this helps with my CI testing
        # if there is a cmdline arg, exit after running the single line snippet, else
        # run like normal
        cmd = code if test else '.q'
        line = input("=> ") if not flag else cmd
        line = line.strip() if not nline else nline
        
        if line not in ('_', '.q', '.st', '.cc'):
            history.append(line)
        elif line == '_':
            if len(history) > 0:
                line = history[-1]
                cprint(f"executing \"{line}\"", 'yellow')
            else:
                cprint('no logged history of commands..', 'yellow')
                continue
        # user requested exit 
        if line == '.q':
            if not test:
                cprint('Arigatōgozaimashita!', 'yellow')
            return res
        # toggle showing syntax tree
        if line == '.st':
            showtree = not showtree
            msg = 'displaying syntax tree' if showtree else 'not displaying syntax tree'
            cprint(msg, 'yellow')
            continue
        # user wants to clear console
        if line == '.cc':
            command = 'clear' if name == 'posix' else 'cls'
            _ = system(command)
            cprint('Flux v0.0.1', 'green')
            continue
        
        # print(line)
        if line[0:3] == ".h":
            try:
                indx = int(line[2:])
                print(indx)
            except ValueError:
                cprint('Index not a valid number.', 'red', 'on_grey')

        tree = SyntaxTree.parse(line)
        # handle any lexing errors
        diag = tree.diagnostics.information
        if diag:
            informOnError(line, diag)
            continue
        # parse the tokens and build a tree
        # handle any parsing errors
        else:
            comp = Compilation(tree)
            result = comp.evaluate(variables)
            diag = result.diagnostics
            res = result.value
            if diag:
                informOnError(line, diag)
                continue
            if not test:
                print(res)

        if showtree:
            print()
            cprint('binder information..', 'yellow')
            binderinfo(result.boundExpr)
            print()
            
            cprint('parser information..', 'yellow')
            print(res)
            prettyprint(tree.root)
        print()
        if flag:
            nline = '.q'

def informOnError(line, diag):
    print()
    for msg in diag:
        print(msg.spantostring(), sep='',end=' -> ')
        cprint(msg.errortostring(), 'yellow')
        prefx = line[0:msg.textspan.start]
        err = line[msg.textspan.start: msg.textspan.end]
        suffx = line[msg.textspan.end:]
        
        print('  '+prefx, end='')
        cprint(err, 'red', 'on_grey', end='')
        print(suffx, end='\n\n')
  
def binderinfo(expr, indent='', is_last=True):
    marker = '└──' if is_last else '├──'    
    # default color
    color = 'magenta'
    
    if isinstance(expr, BBinaryExpression):
        # constructing output 
        out = indent + marker + expr.nodetype().name.upper()
        color = 'magenta'
        cprint(out + ' [type:' + str(expr.type()) + ', operator:' + expr.oper.tokentype.name + ']', color)

        # visit children
        last = expr.composition()[-1]
        indent += '    ' if is_last else '│   '
        for child in expr.composition():
            binderinfo(child, indent, child == last)
    elif isinstance(expr, BUnaryExpression):
        out = indent + marker + expr.nodetype().name.upper()
        color = 'green'
        cprint(out + ' [type:' + str(expr.type()) + ', operator:' + expr.sign.tokentype.name + ']', color)
        indent += '    ' if is_last else '│   '
        binderinfo(expr.operand, indent, True)
        return
    elif isinstance(expr, BAssignmentExpression):
        # constructing output 
        out = indent + marker + expr.nodetype().name.upper()
        color = 'magenta'
        cprint(out + ' [type:' + str(expr.type()) + ', operator:=]', color)

        indent += '    ' if is_last else '│   '
        tokn, iExpr = expr.composition()
        prettyprint(tokn, indent, False)
        binderinfo(iExpr, indent)
    elif isinstance(expr, BLiteralExpression):
        out = indent + marker + expr.nodetype().name.upper()
        color = 'cyan'
        cprint(out + ' [type:' + str(expr.type()) + ', value:' + str(expr.value) + ']', color)
        return
    elif isinstance(expr, BVariableExpression):
        out = indent + marker + expr.nodetype().name.upper()
        color = 'cyan'
        cprint(out + ' [type:' + str(expr.type()) + ', id: ' + str(expr.name) + ', val: ' + str(expr.val) + ']', color)
        return
    # set the indent for the next call
    else: return

# prints the Syntax tree with a nice tree syntax
def prettyprint(node, indent='', is_last=True):
    # the marker is decided based on whether the current node passed in is the last in that level
    marker = '└──' if is_last else '├──'

    # constructing output 
    out = indent + marker + node.nodetype().name.upper()
    # default color
    color = 'white'
    # if we have run into a leaf (Token inside an expression)
    if isinstance(node, Token):
        # numbers get green, other types get cyan
        color = 'green' if node.tokentype is TokenType.number else 'cyan'
        cprint(out + ' [' + str(node.val) + ']', color)
        return 
    cprint(indent + marker + node.nodetype().name.upper(), color)

    # set the indent for the next call
    indent += '    ' if is_last else '│   '

    # visit children
    last = node.getchildren()[-1]
    for child in node.getchildren():
        prettyprint(child, indent, child == last)

if __name__ == '__main__':
    try:
        flag = sys.argv[1]
        flag = True if flag == '-c' else False
        nline = False
    except IndexError:
        flag = False
        nline = False
    entry(flag, nline)