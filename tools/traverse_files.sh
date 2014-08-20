#!/bin/sh
exec </dev/null
exec >log
exec 2>&1
renice +10 -p $$

python traverse_c.py ../trees/trees-c.zip > ../names/names-c.txt

python traverse_java.py ../trees/trees-java.zip > ../names/names-java.txt

python traverse_python.py ../files/files-py.zip > ../names/names-py.txt

