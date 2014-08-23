#!/bin/sh
renice +10 -p $$

python extract_stat.py ../names/names-c.txt > ../stats/stats-c.txt

python extract_stat.py ../names/names-java.txt > ../stats/stats-java.txt

python extract_stat.py -P ../names/names-py.txt > ../stats/stats-py.txt
