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
def find(x, *s):
    for t in x:
        if islist(t):
            if head(t) in s:
                yield t
            else:
                for y in find(t, *s):
                    yield y
    return

def getname(tree):
    if head(tree) == '.primary':
        return issym(tree[1])
    elif head(tree) == '.expression' and len(tree) == 4 and tree[-2] == '..':
        return tree[-1]
    elif head(tree) == '.expression' and len(tree) == 2:
        return getname(tree[1])
    else:
        return None

def traverse_expr(tree):
    for t in walk(tree):
        if head(t) == '.expression' and 4 <= len(t) and t[2] == '.(':
            v = getname(t[1])
            if v:
                r = []
                for tt in find(tail(t), '.expressionList'):
                    for ttt in find(tail(tt), '.expression'):
                        vv = getname(ttt)
                        if vv:
                            r.append(vv)
                        else:
                            r.append(None)
                print 'funcall', v, ' '.join( vv or '*' for vv in r )
        elif head(t) == '.creator':
            v = t[1][1]
            if issym(v):
                r = []
                for tt in find(tail(t), '.expression'):
                    vv = getname(tt)
                    if vv:
                        r.append(vv)
                    else:
                        r.append(None)
                print 'funcall', v, ' '.join( vv or '*' for vv in r )
    return
    
def traverse(tree):
    if not islist(tree): return
    if head(tree) == '.typeDeclaration':
        for t in find(tail(tree), '.classDeclaration'):
            v = issym(t[2])
            if v:
                print 'typedecl', v
            for tt in walk(t):
                if head(tt) == '.memberDeclaration':
                    for ttt in find(tail(tt), '.variableDeclarator'):
                        for tttt in find(tail(ttt), '.variableDeclaratorId'):
                            v = issym(tttt[1])
                            if v:
                                print 'vardecl', v
                        for tttt in find(tail(ttt), '.variableInitializer'):
                            traverse_expr(tttt)
                elif head(tt) == '.methodDeclaration':
                    v = tt[2]
                    if issym(v):
                        r = []
                        for ttt in find(tail(tt), '.variableDeclaratorId'):
                            v = ttt[1]
                            if issym(v):
                                r.append(v)
                        print 'funcdecl', v, ' '.join(r)
                    for ttt in find(tail(tt), '.methodBody'):
                        for tttt in find(tail(ttt), '.variableDeclarator'):
                            for ttttt in find(tail(tttt), '.variableDeclaratorId'):
                                v = issym(ttttt[1])
                                if v:
                                    print 'vardecl', v
                        traverse_expr(ttt)
    else:
        for t in tail(tree):
            traverse(t)
    return

def main(argv):
    for line in fileinput.input():
        parser = SexprParser()
        parser.feed(line.strip())
        for tree in parser.close():
            traverse(tree)
    return 0

if __name__ == '__main__': sys.exit(main(sys.argv))
