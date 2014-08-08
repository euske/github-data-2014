#!/bin/sh

awk '$1=="c" && 1000 <=$3 && $3 < 100000' all-files |
  python shuffle.py | head -n10000 > files-c

awk '$1=="java" && 1000 <=$3 && $3 < 100000' all-files |
  python shuffle.py | head -n10000 > files-java

awk '$1=="py" && 1000 <=$3 && $3 < 100000' all-files |
  python shuffle.py | head -n10000 > files-py
