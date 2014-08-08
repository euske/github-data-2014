#!/usr/bin/env python
#
# usage:
#  $ python json2list.py repo-java.json | awk '{a=$1; gsub(/\//,"-",a); print "wget -O", a "-" $2 ".zip https://github.com/" $1 "/archive/" $2 ".zip";}' | sh
#

import sys
import json

def main(argv):
    args = argv[1:]
    path = args.pop(0)
    fp = open(path)
    obj = json.load(fp)
    fp.close()
    #
    for repo in obj['items']:
        full_name = repo['full_name']
        default_branch = repo['default_branch']
        print full_name, default_branch
    return 0

if __name__ == '__main__': sys.exit(main(sys.argv))
