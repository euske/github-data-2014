#!/usr/bin/env python
import sys
import os
import zipfile
import subprocess

os.environ['CLASSPATH'] = '/usr/share/java/antlr-complete.jar:.'

def fakecpp(lines):
    decl = False
    for line in lines:
        if decl or line.lstrip().startswith('#'):
            decl = line.rstrip().endswith('\\')
        else:
            yield line
    return

def parse_c(data):
    lines = data.splitlines()
    lines = fakecpp(lines)
    proc = subprocess.Popen(['grun','C','compilationUnit','-tree'],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    for line in lines:
        proc.stdin.write(line)
    proc.stdin.close()
    data = proc.stdout.read()
    proc.stdout.close()
    return data

def main(argv):
    args = argv[1:]
    outpath = args.pop(0)
    out = zipfile.ZipFile(outpath, 'w', compression=zipfile.ZIP_DEFLATED)
    for path in args:
        zf = zipfile.ZipFile(path)
        for name in zf.namelist():
            sys.stderr.write('parsing: %r\n' % name)
            sys.stderr.flush()
            data = zf.read(name)
            tree = parse_c(data)
            out.writestr(name+'.tree', tree)
        zf.close()
    out.close()
    return 0

if __name__ == '__main__': sys.exit(main(sys.argv))
