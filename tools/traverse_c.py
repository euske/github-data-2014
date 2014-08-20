#!/usr/bin/env python
import sys
sys.setrecursionlimit(10000)
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

def getname(x):
    while islist(x):
        if head(x) == '.postfixExpression' and len(x) == 4:
            x = x[-1]
        elif len(x) == 2:
            x = x[1]
        else:
            return None
    return x

def traverse(tree):
    if not islist(tree): return
    if head(tree) == '.functionDefinition':
        for t in tail(tree):
            if head(t) == '.declarator':
                r = []
                for tt in find(tail(t), '.directDeclarator'):
                    for tt in walk(tt):
                        if head(tt) == '.directDeclarator':
                            v = issym(tt[1])
                            if v:
                                r.append(v)
                print 'funcdecl', ' '.join(r)
            else:
                traverse(t)
    elif head(tree) == '.externalDeclaration':
        for t in tail(tree):
            if head(t) == '.declaration':
                for tt in tail(t):
                    if head(tt) == '.declarationSpecifiers':
                        r = []
                        typedef = False
                        for ttt in tail(tt):
                            if head(ttt) == '.declarationSpecifier':
                                for tttt in tail(ttt):
                                    if (head(tttt) == '.storageClassSpecifier' and
                                        tttt[1] == '.typedef'):
                                        typedef = True
                                    elif head(tttt) == '.typeSpecifier':
                                        r.append(tttt[1])
                        if typedef and len(r) == 2 and head(r[-1]) == '.typedefName':
                            print 'typedecl', r[-1][1]
                    elif head(tt) == '.initDeclaratorList':
                        r = []
                        for tt in find(tail(t), '.directDeclarator'):
                            for tt in walk(tt):
                                if head(tt) == '.directDeclarator':
                                    v = issym(tt[1])
                                    if v:
                                        r.append(v)
                        print 'funcdecl', ' '.join(r)
                
    elif head(tree) == '.declaration':
        for t in tail(tree):
            if head(t) == '.initDeclaratorList':
                for tt in find(tail(t), '.directDeclarator'):
                    for tt in walk(tt):
                        if head(tt) == '.directDeclarator':
                            v = issym(tt[1])
                            if v and v != '.(':
                                print 'vardecl', v
            else:
                traverse(t)
    elif head(tree) in ('.initializer', '.expression'):
        for t in find(tail(tree), '.postfixExpression'):
            if (3 <= len(t) and
                getname(t[1]) and
                issym(t[2]) == '.('):
                v = getname(t[1])
                r = [v]
                for x in find(t[3:-1], '.assignmentExpression'):
                    v = getname(x)
                    if v:
                        r.append(v)
                    else:
                        r.append('*')
                print 'funcall', ' '.join(r)
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
