#!/usr/bin/env python
import sys
import fileinput
import os.path
import zipfile

def main(argv):
    args = argv[1:]
    outpath = args.pop(0)
    d = {}
    for line in fileinput.input(args):
        (ext,path,size,name) = line.strip().split(' ')
        if path not in d:
            d[path] = []
        d[path].append(name)
    out = zipfile.ZipFile(outpath, 'w')
    for (path,names) in d.iteritems():
        print '--', path
        zf = zipfile.ZipFile(path)
        (name1,_) = os.path.splitext(path)
        for name in names:
            name2 = name.replace('/','_')
            dstname = name1+'_'+name2
            data = zf.read(name)
            out.writestr(dstname, data)
            print name, dstname
        zf.close()
    out.close()
    return 0

if __name__ == '__main__': sys.exit(main(sys.argv))
