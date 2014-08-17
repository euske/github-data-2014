#!/usr/bin/env python
import sys
import zipfile
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
def find1(x, s):
    if x:
        for t in x:
            if head(t) == s: return t
    return None

def getname(tree):
    if head(tree) == '.primary' and len(tree) == 2:
        return issym(tree[1])
    elif head(tree) == '.primary' and len(tree) == 4 and tree[-2] == '..':
        return issym(tree[-1])
    elif head(tree) == '.expression' and len(tree) == 4 and tree[-2] == '..':
        return issym(tree[-1])
    elif head(tree) == '.expression' and len(tree) == 5 and tree[-2] == '.)':
        return getname(tree[-1])
    elif head(tree) == '.expression' and len(tree) == 2:
        return getname(tree[1])
    else:
        return None

def traverse_expr(tree):
    assert head(tree) == '.expression'
    if 4 <= len(tree) and tree[2] == '.(':
        name = getname(tree[1])
        args = []
        tree = find1(tail(tree), '.expressionList')
        if tree:
            for t in tree:
                if head(t) == '.expression':
                    v = getname(t)
                    if v:
                        args.append(v)
                    else:
                        args.append(None)
                    traverse_expr(t)
        print 'funcall', name, ' '.join( v or '*' for v in args )
    elif 3 <= len(tree) and tree[1] == '.new':
        tree = find1(tail(tree), '.creator')
        name = tree[1][1]
        args = []
        t = find1(tail(tree), '.classCreatorRest')
        if t:
            t = find1(tail(t), '.arguments')
            t = find1(tail(t), '.expressionList')
            if t:
                for tt in find(tail(t), '.expression'):
                    v = getname(tt)
                    if v:
                        args.append(v)
                    else:
                        args.append(None)
                    traverse_expr(tt)
        print 'funcall', name, ' '.join( v or '*' for v in args )
    else:
        for t in find(tail(tree), '.expression'):
            traverse_expr(t)
    return

def traverse_var(tree, init=True):
    for t in tail(tree):
        if head(t) == '.variableDeclarator':
            tt = find1(tail(t), '.variableDeclaratorId')
            if tt:
                print 'vardecl', issym(tt[1])
            if init:
                tt = find1(tail(t), '.variableInitializer')
                if tt:
                    for expr in find(tt, '.expression'):
                        traverse_expr(expr)
    return

def traverse_body(tree):
    for t in find(tree, '.variableDeclarators'):
        traverse_var(t, init=False)
    for expr in find(tree, '.expression'):
        traverse_expr(expr)
    return

def traverse_func(tree):
    name = tree[2]
    args = []
    t = find1(tail(tree), '.formalParameters')
    if t:
        t = find1(tail(t), '.formalParameterList')
        if t:
            for tt in t:
                if head(tt) == '.formalParameter':
                    ttt = find1(tail(tt), '.variableDeclaratorId')
                    if ttt:
                        args.append(issym(ttt[1]))
    print 'funcdecl', name, ' '.join(args)
    tree = find1(tail(tree), '.methodBody')
    if tree:
        traverse_body(tree)
    return

def traverse(tree):
    if not islist(tree): return
    if head(tree) == '.typeDeclaration':
        tree = find1(tail(tree), '.classDeclaration')
        if tree:
            print 'typedecl', issym(tree[2])
            tree = find1(tail(tree), '.classBody')
            if tree:
                for t in tail(tree):
                    if head(t) == '.classBodyDeclaration':
                        for tt in tail(t):
                            if head(tt) == '.memberDeclaration':
                                for mem in tail(tt):
                                    if head(mem) == '.fieldDeclaration':
                                        mem = find1(tail(mem), '.variableDeclarators')
                                        if mem:
                                            traverse_var(mem)
                                    elif head(mem) == '.methodDeclaration':
                                        traverse_func(mem)
                            elif head(tt) == '.block':
                                traverse_body(tt)
    else:
        for t in tail(tree):
            traverse(t)
    return

def main(argv):
    args = argv[1:]
    for path in args:
        if path.endswith('.zip'):
            zf = zipfile.ZipFile(path)
            for name in zf.namelist():
                sys.stderr.write('parsing: %r\n' % name)
                sys.stderr.flush()
                data = zf.read(name)
                try:
                    parser = SexprParser()
                    parser.feed(data)
                    for tree in parser.close():
                        traverse(tree)
                except SyntaxError, e:
                    print 'error:', name, e
            zf.close()
        else:
            sys.stderr.write('parsing: %r\n' % path)
            sys.stderr.flush()
            fp = open(path, 'rb')
            for line in fp:
                try:
                    parser = SexprParser()
                    parser.feed(line)
                    for tree in parser.close():
                        traverse(tree)
                except SyntaxError, e:
                    print 'error:', path, e
            fp.close()
    return 0

if __name__ == '__main__': sys.exit(main(sys.argv))
