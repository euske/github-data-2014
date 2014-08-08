#!/usr/bin/env python
import sys
import random
import fileinput

def main(argv):
    lines = list(fileinput.input())
    random.shuffle(lines)
    for line in lines:
        print line.strip()
    return 0

if __name__ == '__main__': sys.exit(main(sys.argv))
