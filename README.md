# flux

[![Build Status](https://dev.azure.com/pepplejoshua/office/_apis/build/status/pepplejoshua.flux?branchName=master)](https://dev.azure.com/pepplejoshua/office/_build/latest?definitionId=1&branchName=master)

## nuggets:
- use type(i) to get the base type of a variable i
- using isinstance(x, Y) does you one better and tells you if x is an instance of Y class
- use termcolor module (cprint, colored) if there is the need to display colored terminal output

## progress:
- lexer works (num, space, ops, parenthesis). it produces the leaves (nodes) from which our parse tree will be built [creates words]
- parser takes lexemes and build an AST (def not optimized) and builds trees [uses words to create sentences]
- parser done and added paren syntax, binary syntax

## ongoing:
- write the type structure for the complex Expression types
- type checking for numbers and boolean

## interpreter commands:
```
Flux v0.0.1
=> .st
displaying syntax tree
=> .st
not displaying syntax tree
=> .q
Arigatōgozaimashita!
```
> **Note:** _.cc_ command clears the terminal of previous inputs

**syntax examples:**
```
Flux v0.0.1
=> 1
1
=> .st
displaying syntax tree
=> 1
1
└──LITERAL_EXPR
    └──NUMBER [1]
=> 1 + 2
3
└──BIN_EXPR
    ├──LITERAL_EXPR
    │   └──NUMBER [1]
    ├──PLUS [+]
    └──LITERAL_EXPR
        └──NUMBER [2]
=> (-1) + (-1)
-2
└──BIN_EXPR
    ├──PAREN_EXPR
    │   ├──OPEN_PAREN [(]
    │   ├──UNARY_EXPR
    │   │   ├──MINUS [-]
    │   │   └──LITERAL_EXPR
    │   │       └──NUMBER [1]
    │   └──CLOSED_PAREN [)]
    ├──PLUS [+]
    └──PAREN_EXPR
        ├──OPEN_PAREN [(]
        ├──UNARY_EXPR
        │   ├──MINUS [-]
        │   └──LITERAL_EXPR
        │       └──NUMBER [1]
        └──CLOSED_PAREN [)]

=> -1
-1
└──UNARY_EXPR
    ├──MINUS [-]
    └──LITERAL_EXPR
        └──NUMBER [1]

=> +1 - 2
-1
└──BIN_EXPR
    ├──UNARY_EXPR
    │   ├──PLUS [+]
    │   └──LITERAL_EXPR
    │       └──NUMBER [1]
    ├──MINUS [-]
    └──LITERAL_EXPR
        └──NUMBER [2]

=> 1 + -1 + 2
2
└──BIN_EXPR
    ├──BIN_EXPR
    │   ├──LITERAL_EXPR
    │   │   └──NUMBER [1]
    │   ├──PLUS [+]
    │   └──UNARY_EXPR
    │       ├──MINUS [-]
    │       └──LITERAL_EXPR
    │           └──NUMBER [1]
    ├──PLUS [+]
    └──LITERAL_EXPR
        └──NUMBER [2]

=> +1*(2^(-2*(-1)))      
4
└──BIN_EXPR
    ├──UNARY_EXPR
    │   ├──PLUS [+]
    │   └──LITERAL_EXPR
    │       └──NUMBER [1]
    ├──MULTIPLY [*]
    └──PAREN_EXPR
        ├──OPEN_PAREN [(]
        ├──BIN_EXPR
        │   ├──LITERAL_EXPR
        │   │   └──NUMBER [2]
        │   ├──EXPONENT [^]
        │   └──PAREN_EXPR
        │       ├──OPEN_PAREN [(]
        │       ├──BIN_EXPR
        │       │   ├──UNARY_EXPR
        │       │   │   ├──MINUS [-]
        │       │   │   └──LITERAL_EXPR
        │       │   │       └──NUMBER [2]
        │       │   ├──MULTIPLY [*]
        │       │   └──PAREN_EXPR
        │       │       ├──OPEN_PAREN [(]
        │       │       ├──UNARY_EXPR
        │       │       │   ├──MINUS [-]
        │       │       │   └──LITERAL_EXPR
        │       │       │       └──NUMBER [1]
        │       │       └──CLOSED_PAREN [)]
        │       └──CLOSED_PAREN [)]
        └──CLOSED_PAREN [)]

=> true and false
False

=> false || true
True

=> (1 == (5-4)) and (1 != 100-22) || false
True
└──BIN_EXPR
    ├──BIN_EXPR
    │   ├──PAREN_EXPR
    │   │   ├──OPEN_PAREN [(]
    │   │   ├──BIN_EXPR
    │   │   │   ├──LITERAL_EXPR
    │   │   │   │   └──NUMBER [1]
    │   │   │   ├──EQUAL [==]
    │   │   │   └──PAREN_EXPR
    │   │   │       ├──OPEN_PAREN [(]
    │   │   │       ├──BIN_EXPR
    │   │   │       │   ├──LITERAL_EXPR
    │   │   │       │   │   └──NUMBER [5]
    │   │   │       │   ├──MINUS [-]
    │   │   │       │   └──LITERAL_EXPR
    │   │   │       │       └──NUMBER [4]
    │   │   │       └──CLOSED_PAREN [)]
    │   │   └──CLOSED_PAREN [)]
    │   ├──AMPERSAND [and]
    │   └──PAREN_EXPR
    │       ├──OPEN_PAREN [(]
    │       ├──BIN_EXPR
    │       │   ├──LITERAL_EXPR
    │       │   │   └──NUMBER [1]
    │       │   ├──NOTEQUAL [!=]
    │       │   └──BIN_EXPR
    │       │       ├──LITERAL_EXPR
    │       │       │   └──NUMBER [100]
    │       │       ├──MINUS [-]
    │       │       └──LITERAL_EXPR
    │       │           └──NUMBER [22]
    │       └──CLOSED_PAREN [)]
    ├──PIPE [||]
    └──LITERAL_EXPR
        └──FALSE [False]

=> abcsdcdfvsdvscd
0:15 >> ERROR: Unknown identifier [abcsdcdfvsdvscd]

=> .q
Arigatōgozaimashita!
```