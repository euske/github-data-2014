#!/bin/sh
renice +10 -p $$

python extract_stat.py ../names/names-c.txt > ../stats/stat-c.txt

python extract_stat.py ../names/names-java.txt > ../stats/stat-java.txt

python extract_stat.py -P ../names/names-py.txt > ../stats/stat-py.txt
