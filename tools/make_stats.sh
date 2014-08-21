#!/bin/sh
exec </dev/null
exec >log
exec 2>&1
renice +10 -p $$

python extract_stat.py ../names/names-c.txt > stat-c.txt

python extract_stat.py ../names/names-java.txt > stat-java.txt

python extract_stat.py ../names/names-py.txt > stat-py.txt
