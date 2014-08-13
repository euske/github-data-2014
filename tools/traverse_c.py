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
    for t in x:
        if islist(t):
            yield t
            for y in walk(t):
                yield y
    return

def traverse_c(tree):
    if not islist(tree): return
    if head(tree) == '.functionDefinition':
        for t in tail(tree):
            if head(t) == '.declarator':
                r = []
                for tt in walk(tail(t)):
                    if head(tt) == '.directDeclarator':
                        v = issym(tt[1])
                        if v:
                            r.append(v)
                print 'funcdecl', ' '.join(r)
            else:
                traverse_c(t)
    elif head(tree) == '.declaration':
        #pp(tree); print
        for t in tail(tree):
            if head(t) == '.initDeclaratorList':
                r = []
                for tt in walk(tail(t)):
                    if head(tt) == '.directDeclarator':
                        v = issym(tt[1])
                        print 'vardecl', v
            else:
                traverse_c(t)
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
