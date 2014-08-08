#!/usr/bin/env python
import sys
import fileinput
import os.path
import zipfile

def main(argv):
    args = argv[1:]
    outpath = args.pop(0)
    out = zipfile.ZipFile(outpath, 'w')
    for line in fileinput.input(args):
        (ext,path,size,name) = line.strip().split(' ')
        (name1,_) = os.path.splitext(path)
        name2 = name.replace('/','_')
        dstname = name1+'_'+name2
        zf = zipfile.ZipFile(path)
        data = zf.read(name)
        out.writestr(dstname, data)
        print path, name, dstname
        zf.close()
    out.close()
    return 0

if __name__ == '__main__': sys.exit(main(sys.argv))
