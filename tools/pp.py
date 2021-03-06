#!/usr/bin/env python
import sys
import fileinput
from sexpr import SexprParser

def islist(x): return isinstance(x, list) and x

def pp(tree, i=0, out=sys.stdout):
    assert islist(tree), tree
    out.write('(%s' % tree[0])
    i += 1
    for t in tree[1:]:
        out.write('\n'+i*' ')
        if islist(t):
            pp(t, i=i, out=out)
        elif t:
            out.write(t)
    out.write(')')
    return

def main(argv):
    for line in fileinput.input():
        parser = SexprParser()
        parser.feed(line.strip())
        for tree in parser.close():
            if islist(tree):
                pp(tree)
    return 0

if __name__ == '__main__': sys.exit(main(sys.argv))
