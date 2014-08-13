#!/usr/bin/env python
import sys
import fileinput
from sexpr import SexprParser
from pp import pp

def islist(x): return isinstance(x, list) and x
def isstr(x): return isinstance(x, str) and x.startswith('@') and x
def issym(x): return isinstance(x, str) and x.startswith('.') and x
def head(x): return islist(x) and issym(x[0])
def tail(x): return islist(x) and x[1:]
def walk(x):
    yield x
    if islist(x):
        for t in x:
            for y in walk(t):
                yield y
    return 
def find(x, s):
    for t in x:
        if islist(t):
            if head(t) == s:
                yield t
            else:
                for y in find(t, s):
                    yield y
    return

def issingle(x):
    while islist(x):
        if len(x) != 2: return None
        x = x[1]
    return x

def traverse_c(tree):
    if not islist(tree): return
    if head(tree) == '.functionDefinition':
        for t in tail(tree):
            if head(t) == '.declarator':
                #pp(t);print
                r = []
                for tt in walk(t):
                    if head(tt) == '.directDeclarator':
                        v = issym(tt[1])
                        if v:
                            r.append(v)
                print 'funcdecl', ' '.join(r)
            else:
                traverse_c(t)
    elif head(tree) == '.declaration':
        for t in tail(tree):
            if head(t) == '.initDeclaratorList':
                r = []
                for tt in find(tail(t), '.directDeclarator'):
                    v = issym(tt[1])
                    if v:
                        print 'vardecl', v
            else:
                traverse_c(t)
    elif head(tree) in ('.initializer', '.expression'):
        for t in find(tail(tree), '.postfixExpression'):
            if (3 <= len(t) and
                issingle(t[1]) and
                issym(t[2]) == '.('):
                v = issingle(t[1])
                r = [v]
                for x in find(t[3:-1], '.assignmentExpression'):
                    v = issingle(x)
                    if issym(v):
                        r.append(v)
                    else:
                        r.append('*')
                print 'expr', ' '.join(r)
    else:
        for t in tail(tree):
            traverse_c(t)
    return

def main(argv):
    for line in fileinput.input():
        parser = SexprParser()
        parser.feed(line.strip())
        for tree in parser.close():
            traverse_c(tree)
    return 0

if __name__ == '__main__': sys.exit(main(sys.argv))
