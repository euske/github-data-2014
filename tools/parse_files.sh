#!/bin/sh
exec </dev/null
exec >log
exec 2>&1
renice +10 -p $$

python parse_c.py ../trees/trees-c.zip ../files/files-c.zip

python parse_java.py ../trees/trees-java.zip ../files/files-java.zip
