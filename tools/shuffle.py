#!/usr/bin/env python
import sys
import random
import fileinput

N = 100

def main(argv):
    lines = list(fileinput.input())
    random.shuffle(lines)
    d = {}
    for line in lines:
        (t,repo,size,path) = line.strip().split(' ')
        if repo in d and N <= d[repo]: continue
        if repo not in d:
            d[repo] = 0
        d[repo] += 1
        print t, repo, size, path
    return 0

if __name__ == '__main__': sys.exit(main(sys.argv))
