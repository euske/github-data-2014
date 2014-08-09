#!/usr/bin/env python
import sys
import os.path
import zipfile

def main(argv):
    for path in argv[1:]:
        zf = zipfile.ZipFile(path)
        for info in zf.infolist():
            # avoid non-ASCII names.
            try:
                name = info.filename.encode('ascii')
            except UnicodeError:
                continue
            if ' ' in name: continue
            (_,ext) = os.path.splitext(name)
            if ext in ('.c', '.py', '.java'):
                print ext[1:], path, info.file_size, name
        zf.close()
    return 0

if __name__ == '__main__': sys.exit(main(sys.argv))
