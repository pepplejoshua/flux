from parser import Parser
from token import *
from expressionevaluator import ExpressionEvaluator
from os import name, system

def main():
    # get single line and then tokenize repeatedly > repl

    cprint('Flux v0.0.1', 'green')
    showtree = True
    while True:
        # init lexer
        line = input("=> ")

        # user requested exit 
        if line == '.q':
            cprint('Arigatōgozaimashita!', 'yellow')
            break
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
 
        parser = Parser(line)
        if parser.error:
            for msg in parser.diagnostics:
                cprint(msg, 'red', 'on_grey')
            continue
        # parse the tokens and build a tree
        tree = parser.parse()
        
        if parser.error:
            for msg in parser.diagnostics:
                cprint(msg, 'red', 'on_grey')
            continue
        else:
            eval = ExpressionEvaluator(tree.root)
            res = eval.evaluate()
            print(res)

        if showtree:
            prettyprint(tree.root)

# prints the Syntax tree with a nice tree syntax
def prettyprint(node, indent='', is_last=True):
    # the marker is decided based on whether the current node passed in is the last in that level
    marker = '└──' if is_last else '├──'

    # constructing output 
    out = indent + marker + node.nType().name.upper()
    # default color
    color = 'magenta'
    # if we have run into a leaf (Token inside an expression)
    if isinstance(node, Token):
        # numbers get green, other types get cyan
        color = 'green' if node.token_t is TokenType.number else 'cyan'
        cprint(out + ' [' + str(node.val) + ']', color)
        return 
    cprint(indent + marker + node.nType().name.upper(), color)

    # set the indent for the next call
    indent += '    ' if is_last else '│   '

    # visit children
    last = node.getchildren()[-1]
    for child in node.getchildren():
        prettyprint(child, indent, child == last)

main()