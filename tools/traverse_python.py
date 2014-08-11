#!/usr/bin/env python
import sys
import zipfile
import ast

def traverse_python(tree):
    print tree
    return

def main(argv):
    args = argv[1:]
    for path in args:
        zf = zipfile.ZipFile(path)
        for name in zf.namelist():
            sys.stderr.write('parsing: %r\n' % name)
            sys.stderr.flush()
            data = zf.read(name)
            try:
                tree = ast.parse(data)
                traverse_python(tree)
            except SyntaxError, e:
                print 'error:', name, e
        zf.close()
    return 0

if __name__ == '__main__': sys.exit(main(sys.argv))
